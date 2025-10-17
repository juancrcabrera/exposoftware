from pymongo import MongoClient
from config import Config
import bcrypt

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DB_NAME]

# Crear admin
admin_data = {
    "username": "admin",
    "email": "admin@tradeco.com",
    "password": bcrypt.hashpw("Admin123".encode('utf-8'), bcrypt.gensalt()),
    "nombre": "Administrador",
    "telefono": "",
    "direccion": "",
    "role": "admin",
    "active": True
}

result = db.users.insert_one(admin_data)
print(f"✅ Admin creado: {result.inserted_id}")