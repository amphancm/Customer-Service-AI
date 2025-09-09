from flask import Blueprint
from controllers.upload_controller import upload_file, delete_file, list_files, get_file
from flask_jwt_extended import jwt_required

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/documents", methods=["POST"])
@jwt_required()  
def upload():
    return upload_file()

@upload_bp.route("/documents/<file_id>", methods=["DELETE"])
@jwt_required()
def delete(file_id):
    return delete_file(file_id)

@upload_bp.route("/documents", methods=["GET"])
@jwt_required()
def list_docs():
    return list_files()

@upload_bp.route("/documents/<file_id>", methods=["GET"])
@jwt_required()
def view_file(file_id):
    return get_file(file_id)