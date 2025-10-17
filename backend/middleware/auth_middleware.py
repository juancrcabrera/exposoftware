from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar token en el header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de token inválido'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        try:
            # Decodificar el token
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
            current_user_role = data.get('role', 'usuario')
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expirado'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            }), 401
        
        # Pasar el ID del usuario a la función
        return f(current_user_id, current_user_role, *args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Formato de token inválido'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no proporcionado'
            }), 401
        
        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
            current_user_role = data.get('role', 'usuario')
            
            # Verificar que sea admin
            if current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Acceso denegado. Se requiere rol de administrador'
                }), 403
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expirado'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            }), 401
        
        return f(current_user_id, current_user_role, *args, **kwargs)
    
    return decorated