from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from middleware.auth_middleware import token_required, admin_required
from utils.validators import allowed_file, validate_product_data, sanitize_filename
from config import Config

products_bp = Blueprint('products', __name__)

def init_routes(db, product_model, user_model):
    """Inicializar rutas de productos"""
    
    @products_bp.route('/', methods=['GET'])
    def get_products():
        """Obtener todos los productos con paginación y filtros"""
        try:
            # Parámetros de paginación
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            skip = (page - 1) * limit
            
            # Filtros opcionales
            filters = {}
            categoria = request.args.get('categoria')
            search = request.args.get('search')
            
            if categoria:
                filters['categoria'] = categoria
            
            # Buscar productos
            if search:
                products = product_model.search(search, skip, limit)
            else:
                products = product_model.find_all(skip, limit, filters)
            
            # Convertir a diccionario
            products_list = [product_model.to_dict(p) for p in products]
            
            # Contar total
            total = product_model.count(filters)
            
            return jsonify({
                'success': True,
                'data': {
                    'products': products_list,
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
                'message': f'Error al obtener productos: {str(e)}'
            }), 500
    
    @products_bp.route('/<product_id>', methods=['GET'])
    def get_product(product_id):
        """Obtener un producto específico"""
        try:
            product = product_model.find_by_id(product_id)
            
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Producto no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': product_model.to_dict(product)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener producto: {str(e)}'
            }), 500
    
    @products_bp.route('/', methods=['POST'])
    @token_required
    def create_product(current_user_id, current_user_role):
        """Crear un nuevo producto"""
        try:
            # Obtener datos del formulario
            data = request.form.to_dict()
            
            # Validar datos del producto
            valid, errors = validate_product_data(data)
            if not valid:
                return jsonify({
                    'success': False,
                    'message': 'Datos inválidos',
                    'errors': errors
                }), 400
            
            # Manejar imagen
            imagen_url = ""
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename and allowed_file(file.filename):
                    filename = sanitize_filename(file.filename)
                    # Agregar timestamp para evitar colisiones
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    imagen_url = f"/uploads/products/{filename}"
            
            # Obtener username del usuario
            user = user_model.find_by_id(current_user_id)
            data['username'] = user.get('username', 'Anónimo')
            data['imagen_url'] = imagen_url
            
            # Crear producto
            product_id = product_model.create(data, current_user_id)
            
            # Obtener producto creado
            product = product_model.find_by_id(product_id)
            
            return jsonify({
                'success': True,
                'message': 'Producto publicado exitosamente',
                'data': product_model.to_dict(product)
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al crear producto: {str(e)}'
            }), 500
    
    @products_bp.route('/<product_id>', methods=['PUT'])
    @token_required
    def update_product(current_user_id, current_user_role, product_id):
        """Actualizar un producto existente"""
        try:
            # Verificar que el producto existe
            product = product_model.find_by_id(product_id)
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Producto no encontrado'
                }), 404
            
            # Verificar que el usuario es el dueño (o admin)
            if product['user_id'] != current_user_id and current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'No tienes permiso para editar este producto'
                }), 403
            
            # Obtener datos del formulario
            data = request.form.to_dict()
            
            # Validar datos si se proporcionan
            if data:
                valid, errors = validate_product_data(data)
                if not valid:
                    return jsonify({
                        'success': False,
                        'message': 'Datos inválidos',
                        'errors': errors
                    }), 400
            
            # Manejar nueva imagen si se proporciona
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename and allowed_file(file.filename):
                    filename = sanitize_filename(file.filename)
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    data['imagen_url'] = f"/uploads/products/{filename}"
                    
                    # Eliminar imagen anterior si existe
                    if product.get('imagen_url'):
                        old_file = product['imagen_url'].replace('/uploads/products/', '')
                        old_filepath = os.path.join(Config.UPLOAD_FOLDER, old_file)
                        if os.path.exists(old_filepath):
                            os.remove(old_filepath)
            
            # Actualizar producto
            success = product_model.update(product_id, data, current_user_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'No se pudo actualizar el producto'
                }), 400
            
            # Obtener producto actualizado
            updated_product = product_model.find_by_id(product_id)
            
            return jsonify({
                'success': True,
                'message': 'Producto actualizado exitosamente',
                'data': product_model.to_dict(updated_product)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al actualizar producto: {str(e)}'
            }), 500
    
    @products_bp.route('/<product_id>', methods=['DELETE'])
    @token_required
    def delete_product(current_user_id, current_user_role, product_id):
        """Eliminar un producto"""
        try:
            # Verificar que el producto existe
            product = product_model.find_by_id(product_id)
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Producto no encontrado'
                }), 404
            
            # Verificar que el usuario es el dueño (o admin)
            if product['user_id'] != current_user_id and current_user_role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'No tienes permiso para eliminar este producto'
                }), 403
            
            # Eliminar imagen si existe
            if product.get('imagen_url'):
                filename = product['imagen_url'].replace('/uploads/products/', '')
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            # Eliminar producto
            success = product_model.delete(product_id, current_user_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'No se pudo eliminar el producto'
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Producto eliminado exitosamente'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al eliminar producto: {str(e)}'
            }), 500
    
    @products_bp.route('/categories', methods=['GET'])
    def get_categories():
        """Obtener todas las categorías disponibles"""
        try:
            from models.product import Product
            return jsonify({
                'success': True,
                'data': Product.CATEGORIES
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener categorías: {str(e)}'
            }), 500
    
    @products_bp.route('/user/<user_id>', methods=['GET'])
    def get_user_products(user_id):
        """Obtener productos de un usuario específico"""
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
            skip = (page - 1) * limit
            
            products = product_model.find_by_user(user_id, skip, limit)
            products_list = [product_model.to_dict(p) for p in products]
            
            return jsonify({
                'success': True,
                'data': products_list
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener productos del usuario: {str(e)}'
            }), 500
    
    return products_bp