import os
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from db import Connection
from datetime import datetime
from toolcalling import load_docs
from bson import ObjectId

mongo = Connection('otg_db')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "documents")
UPLOAD_FOLDER = os.path.normpath(UPLOAD_FOLDER) 
ALLOWED_EXTENSIONS = {"pdf", "csv", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        original_filename = file.filename  # keep Thai name
        stored_filename = secure_filename(original_filename)

        # Fallback: if secure_filename strips everything (like only ".pdf")
        if stored_filename == "" or stored_filename == original_filename.split(".")[-1]:
            ext = os.path.splitext(original_filename)[1]
            stored_filename = f"file_{datetime.utcnow().timestamp()}{ext}"

        filepath = os.path.join(UPLOAD_FOLDER, stored_filename)
        file.save(filepath)

        try:
            load_docs()
        except Exception as e:
            return jsonify({"error": f"Failed to load document: {str(e)}"}), 500

        result = mongo.doc_files.insert_one({
            "original_filename": original_filename,   # Thai visible name
            "stored_filename": stored_filename,       # disk-safe name
            "path": filepath,
            "uploaded_at": datetime.utcnow()
        })

        return jsonify({
            "message": "File uploaded successfully",
            "id": str(result.inserted_id),
            "filename": original_filename,   # return Thai name to frontend
            "path": filepath
        }), 201

    return jsonify({"error": "File type not allowed"}), 400


def delete_file(file_id):
    """Delete file by Mongo _id and remove from disk"""
    try:
        doc = mongo.doc_files.find_one({"_id": ObjectId(file_id)})
        if not doc:
            return jsonify({"error": "File not found"}), 404

        # Remove file from disk if exists
        filepath = doc.get("path")
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

        # Remove record from Mongo
        mongo.doc_files.delete_one({"_id": ObjectId(file_id)})

        return jsonify({
            "message": "File deleted successfully",
            "id": file_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def list_files():
    data = mongo.doc_files.find()
    resp = [
        {
            "id": str(item.get("_id")),
            "filename": item.get("original_filename") or item.get("stored_filename") or "Unknown",
            "path": item.get("path", ""),
            "uploaded_at": item.get("uploaded_at").isoformat() if item.get("uploaded_at") else None
        }
        for item in data
    ]
    return jsonify(resp), 200


def get_file(file_id):
    try:
        file = mongo.doc_files.find_one({"_id": ObjectId(file_id)})
        if not file:
            return jsonify({"error": "File not found"}), 404

        filepath = file.get("path")
        if filepath and os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=file.get("original_filename")
            )
        else:
            return jsonify({"error": "File missing on disk"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
