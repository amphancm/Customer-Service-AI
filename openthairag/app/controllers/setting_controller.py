from db import Connection
from flask import Flask, request, jsonify
from bson import ObjectId
from bson.json_util import dumps

mongo=Connection('otg_db')

def setting_post(data):
    result = mongo.setting.insert_one(data)
    print(result)
    return jsonify({
        "message": "Data inserted successfully", 
        "id": str(result.inserted_id) 
    }), 201
    
def setting_patch(data):
    update_fields = {
        'line_activate': data.get('line_activate', False),
        'fb_activate': data.get('fb_activate', False),
        'product_activate': data.get('product_activate', False),
        'feedback_activate': data.get('feedback_activate', False),
        'greeting_activate': data.get('greeting_activate', False),
        'line_key': data.get('line_key', ''),
        'line_secret': data.get('line_secret', ''),
        'facebook_token': data.get('facebook_token', ''),
        'facebook_verify_password': data.get('facebook_verify_password', ''),
        'greeting_prompt': data.get('greeting_prompt', ''),
    }
    
    # Handle server object
    if 'server' in data:
        update_fields['server'] = {
            'enabled': data['server'].get('enabled', False),
            'domainname': data['server'].get('domainname', ''),
            'apikey': data['server'].get('apikey', ''),
            'modelname': data['server'].get('modelname', '')
        }
    
    # Handle local object
    if 'local' in data:
        update_fields['local'] = {
            'enabled': data['local'].get('enabled', False),
            'domainname': data['local'].get('domainname', ''),
            'apikey': data['local'].get('apikey', ''),
            'modelname': data['local'].get('modelname', '')
        }
    
    result = mongo.setting.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set": update_fields
    })
    
    return jsonify({
        "message": "Data updated successfully", 
    }), 201

def setting_get():
    data = mongo.setting.find()
    return dumps(data), 200

def system_prompt_post(data):
    result = mongo.systemPrompt.insert_one(data)
    return jsonify({
        "message": "Data inserted successfully", 
        "id": str(result.inserted_id) 
    }), 201

def system_prompt_patch(data):
    result = mongo.systemPrompt.update_one({
        '_id': ObjectId(data['id'])
    },
    {
        "$set":{
            'content': data['content'] if 'content' in data else '',
            'temperature': data['temperature'] if 'temperature' in data else 0.4,
        }
    })
    return jsonify({
        "message": "Data updated successfully", 
    }), 201

def system_prompt_get():
    data = mongo.systemPrompt.find_one()
    return dumps(data), 200
