from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    """Modelo de Usuario para MongoDB"""
    
    def __init__(self, db):
        self.collection = db.users
        self._create_indexes()
    
    def _create_indexes(self):
        """Crear índices para búsquedas eficientes"""
        self.collection.create_index("email", unique=True)
        self.collection.create_index("username", unique=True)
    
    def create(self, data):
        """Crear un nuevo usuario"""
        user_data = {
            "username": data.get("username"),
            "email": data.get("email"),
            "password": self._hash_password(data.get("password")),
            "nombre": data.get("nombre"),
            "telefono": data.get("telefono", ""),
            "direccion": data.get("direccion", ""),
            "role": data.get("role", "usuario"),  # usuario o admin
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "active": True
        }
        
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        """Buscar usuario por email"""
        return self.collection.find_one({"email": email})
    
    def find_by_username(self, username):
        """Buscar usuario por username"""
        return self.collection.find_one({"username": username})
    
    def find_by_id(self, user_id):
        """Buscar usuario por ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(user_id)})
        except:
            return None
    
    def update(self, user_id, data):
        """Actualizar datos del usuario"""
        update_data = {
            "updated_at": datetime.utcnow()
        }
        
        # Campos que se pueden actualizar
        allowed_fields = ["nombre", "telefono", "direccion"]
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def verify_password(self, email, password):
        """Verificar contraseña de usuario"""
        user = self.find_by_email(email)
        if not user:
            return None
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user
        return None
    
    def _hash_password(self, password):
        """Hashear contraseña con bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def to_dict(self, user):
        """Convertir usuario a diccionario sin datos sensibles"""
        if not user:
            return None
        
        return {
            "id": str(user["_id"]),
            "username": user.get("username"),
            "email": user.get("email"),
            "nombre": user.get("nombre"),
            "telefono": user.get("telefono", ""),
            "direccion": user.get("direccion", ""),
            "role": user.get("role", "usuario"),
            "created_at": user.get("created_at").isoformat() if user.get("created_at") else None
        }