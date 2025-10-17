// Script de inicialización de MongoDB
// Se ejecuta automáticamente cuando se crea el contenedor

db = db.getSiblingDB('tradeco_db');

// Crear colecciones
db.createCollection('users');
db.createCollection('products');

// Crear índices para users
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "username": 1 }, { unique: true });

// Crear índices para products
db.products.createIndex({ "user_id": 1 });
db.products.createIndex({ "categoria": 1 });
db.products.createIndex({ "created_at": -1 });
db.products.createIndex({ "nombre": "text", "descripcion": "text" });

print('✅ Base de datos tradeco_db inicializada correctamente');
print('✅ Colecciones e índices creados');