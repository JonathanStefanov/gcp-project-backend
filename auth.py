from flask import request, jsonify
from dotenv import load_dotenv
from functools import wraps
import os 

load_dotenv()

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        expected_token = os.getenv('SECRET_TOKEN')
        if not token or token != expected_token:
            return jsonify({"error": "Authorization token is missing or invalid"}), 403
        return f(*args, **kwargs)

    return decorated