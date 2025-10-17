import re
from werkzeug.utils import secure_filename
from config import Config

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validar contraseña:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe tener al menos una letra mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe tener al menos una letra minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe tener al menos un número"
    
    return True, "Contraseña válida"

def validate_phone(phone):
    """Validar número de teléfono (Argentina)"""
    if not phone:
        return True  # El teléfono es opcional
    
    # Remover espacios y guiones
    phone = phone.replace(" ", "").replace("-", "")
    
    # Validar formato argentino (con o sin código de país)
    pattern = r'^(\+54|0)?[1-9]\d{9,10}$'
    return re.match(pattern, phone) is not None

def validate_username(username):
    """
    Validar nombre de usuario:
    - Entre 3 y 20 caracteres
    - Solo letras, números y guiones bajos
    """
    if len(username) < 3 or len(username) > 20:
        return False, "El nombre de usuario debe tener entre 3 y 20 caracteres"
    
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, "Nombre de usuario válido"

def allowed_file(filename):
    """Verificar si la extensión del archivo está permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_product_data(data):
    """Validar datos de un producto"""
    errors = []
    
    if not data.get('nombre') or len(data['nombre'].strip()) == 0:
        errors.append("El nombre del producto es obligatorio")
    
    if not data.get('categoria'):
        errors.append("La categoría es obligatoria")
    
    if 'precio' in data:
        try:
            precio = float(data['precio'])
            if precio < 0:
                errors.append("El precio no puede ser negativo")
        except (ValueError, TypeError):
            errors.append("El precio debe ser un número válido")
    
    return len(errors) == 0, errors

def sanitize_filename(filename):
    """Limpiar nombre de archivo"""
    return secure_filename(filename)