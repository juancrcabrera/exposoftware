from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from config import Config
from utils.validators import validate_email, validate_password, validate_username, validate_phone

auth_bp = Blueprint('auth', __name__)

def init_routes(db, user_model):
    """Inicializar rutas de autenticación"""
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        """Registro de nuevo usuario"""
        try:
            data = request.get_json()
            
            # Validar campos obligatorios
            required_fields = ['username', 'email', 'password', 'nombre']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'El campo {field} es obligatorio'
                    }), 400
            
            # Validar email
            if not validate_email(data['email']):
                return jsonify({
                    'success': False,
                    'message': 'Email inválido'
                }), 400
            
            # Validar username
            valid, message = validate_username(data['username'])
            if not valid:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            # Validar contraseña
            valid, message = validate_password(data['password'])
            if not valid:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            # Validar teléfono si se proporciona
            if data.get('telefono') and not validate_phone(data['telefono']):
                return jsonify({
                    'success': False,
                    'message': 'Número de teléfono inválido'
                }), 400
            
            # Verificar si el email ya existe
            if user_model.find_by_email(data['email']):
                return jsonify({
                    'success': False,
                    'message': 'El email ya está registrado'
                }), 400
            
            # Verificar si el username ya existe
            if user_model.find_by_username(data['username']):
                return jsonify({
                    'success': False,
                    'message': 'El nombre de usuario ya está en uso'
                }), 400
            
            # Crear usuario
            user_id = user_model.create(data)
            
            # Obtener usuario creado
            user = user_model.find_by_id(user_id)
            
            # Generar token JWT
            token = jwt.encode({
                'user_id': user_id,
                'role': user.get('role', 'usuario'),
                'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
            }, Config.JWT_SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'data': {
                    'token': token,
                    'user': user_model.to_dict(user)
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al registrar usuario: {str(e)}'
            }), 500
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """Login de usuario"""
        try:
            data = request.get_json()
            
            # Validar campos obligatorios
            if not data.get('email') or not data.get('password'):
                return jsonify({
                    'success': False,
                    'message': 'Email y contraseña son obligatorios'
                }), 400
            
            # Verificar credenciales
            user = user_model.verify_password(data['email'], data['password'])
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Email o contraseña incorrectos'
                }), 401
            
            # Verificar si el usuario está activo
            if not user.get('active', True):
                return jsonify({
                    'success': False,
                    'message': 'Usuario inactivo'
                }), 401
            
            # Generar token JWT
            token = jwt.encode({
                'user_id': str(user['_id']),
                'role': user.get('role', 'usuario'),
                'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
            }, Config.JWT_SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'data': {
                    'token': token,
                    'user': user_model.to_dict(user)
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al iniciar sesión: {str(e)}'
            }), 500
    
    return auth_bp