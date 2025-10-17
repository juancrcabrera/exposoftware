from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required, admin_required
from utils.validators import validate_phone

users_bp = Blueprint('users', __name__)

def init_routes(db, user_model):
    """Inicializar rutas de usuarios"""
    
    @users_bp.route('/profile', methods=['GET'])
    @token_required
    def get_profile(current_user_id, current_user_role):
        """Obtener perfil del usuario actual"""
        try:
            user = user_model.find_by_id(current_user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': user_model.to_dict(user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener perfil: {str(e)}'
            }), 500
    
    @users_bp.route('/profile', methods=['PUT'])
    @token_required
    def update_profile(current_user_id, current_user_role):
        """Actualizar perfil del usuario actual"""
        try:
            data = request.get_json()
            
            # Validar teléfono si se proporciona
            if data.get('telefono') and not validate_phone(data['telefono']):
                return jsonify({
                    'success': False,
                    'message': 'Número de teléfono inválido'
                }), 400
            
            # Actualizar usuario
            success = user_model.update(current_user_id, data)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'No se pudo actualizar el perfil'
                }), 400
            
            # Obtener usuario actualizado
            updated_user = user_model.find_by_id(current_user_id)
            
            return jsonify({
                'success': True,
                'message': 'Perfil actualizado exitosamente',
                'data': user_model.to_dict(updated_user)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al actualizar perfil: {str(e)}'
            }), 500
    
    @users_bp.route('/<user_id>', methods=['GET'])
    def get_user(user_id):
        """Obtener información pública de un usuario"""
        try:
            user = user_model.find_by_id(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 404
            
            # Devolver solo información pública
            public_info = {
                'id': str(user['_id']),
                'username': user.get('username'),
                'nombre': user.get('nombre'),
                'created_at': user.get('created_at').isoformat() if user.get('created_at') else None
            }
            
            return jsonify({
                'success': True,
                'data': public_info
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener usuario: {str(e)}'
            }), 500
    
    @users_bp.route('/', methods=['GET'])
    @admin_required
    def get_all_users(current_user_id, current_user_role):
        """Obtener todos los usuarios (solo admin)"""
        try:
            # Parámetros de paginación
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            skip = (page - 1) * limit
            
            # Obtener usuarios
            users = list(user_model.collection.find().skip(skip).limit(limit))
            total = user_model.collection.count_documents({})
            
            # Convertir a diccionario
            users_list = [user_model.to_dict(u) for u in users]
            
            return jsonify({
                'success': True,
                'data': {
                    'users': users_list,
                    'pagination': {
                        'page': page,
                        'limit': limit,
                        'total': total,
                        'pages': (total + limit - 1) // limit
                    }
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener usuarios: {str(e)}'
            }), 500
    
    return users_bp