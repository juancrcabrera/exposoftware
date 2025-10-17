from datetime import datetime
from bson import ObjectId

class Product:
    """Modelo de Producto para MongoDB"""
    
    CATEGORIES = ["Remeras", "Abrigos", "Pantalones", "Vestidos", "Calzado", "Accesorios"]
    
    def __init__(self, db):
        self.collection = db.products
        self._create_indexes()
    
    def _create_indexes(self):
        """Crear índices para búsquedas eficientes"""
        self.collection.create_index("user_id")
        self.collection.create_index("categoria")
        self.collection.create_index("created_at")
        self.collection.create_index([("nombre", "text"), ("descripcion", "text")])
    
    def create(self, data, user_id):
        """Crear un nuevo producto"""
        product_data = {
            "nombre": data.get("nombre"),
            "descripcion": data.get("descripcion", ""),
            "precio": float(data.get("precio", 0)),
            "talla": data.get("talla", ""),
            "categoria": data.get("categoria"),
            "imagen_url": data.get("imagen_url", ""),
            "user_id": user_id,
            "username": data.get("username", ""),
            "estado": "disponible",  # disponible, vendido, reservado
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)
    
    def find_all(self, skip=0, limit=20, filters=None):
        """Obtener todos los productos con paginación"""
        query = filters or {}
        query["estado"] = "disponible"
        
        products = self.collection.find(query)\
            .sort("created_at", -1)\
            .skip(skip)\
            .limit(limit)
        
        return list(products)
    
    def find_by_id(self, product_id):
        """Buscar producto por ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(product_id)})
        except:
            return None
    
    def find_by_user(self, user_id, skip=0, limit=20):
        """Obtener productos de un usuario específico"""
        products = self.collection.find({"user_id": user_id})\
            .sort("created_at", -1)\
            .skip(skip)\
            .limit(limit)
        
        return list(products)
    
    def search(self, query_text, skip=0, limit=20):
        """Buscar productos por texto"""
        products = self.collection.find(
            {"$text": {"$search": query_text}, "estado": "disponible"}
        ).skip(skip).limit(limit)
        
        return list(products)
    
    def filter_by_category(self, categoria, skip=0, limit=20):
        """Filtrar productos por categoría"""
        products = self.collection.find(
            {"categoria": categoria, "estado": "disponible"}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        return list(products)
    
    def update(self, product_id, data, user_id):
        """Actualizar un producto (solo el dueño)"""
        update_data = {"updated_at": datetime.utcnow()}
        
        allowed_fields = ["nombre", "descripcion", "precio", "talla", "categoria", "imagen_url"]
        for field in allowed_fields:
            if field in data:
                if field == "precio":
                    update_data[field] = float(data[field])
                else:
                    update_data[field] = data[field]
        
        result = self.collection.update_one(
            {"_id": ObjectId(product_id), "user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete(self, product_id, user_id):
        """Eliminar un producto (solo el dueño)"""
        result = self.collection.delete_one({
            "_id": ObjectId(product_id),
            "user_id": user_id
        })
        return result.deleted_count > 0
    
    def change_status(self, product_id, status, user_id):
        """Cambiar estado del producto"""
        result = self.collection.update_one(
            {"_id": ObjectId(product_id), "user_id": user_id},
            {"$set": {"estado": status, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def count(self, filters=None):
        """Contar productos"""
        query = filters or {}
        return self.collection.count_documents(query)
    
    def to_dict(self, product):
        """Convertir producto a diccionario"""
        if not product:
            return None
        
        return {
            "id": str(product["_id"]),
            "nombre": product.get("nombre"),
            "descripcion": product.get("descripcion", ""),
            "precio": product.get("precio", 0),
            "talla": product.get("talla", ""),
            "categoria": product.get("categoria"),
            "imagen_url": product.get("imagen_url", ""),
            "user_id": product.get("user_id"),
            "username": product.get("username", ""),
            "estado": product.get("estado", "disponible"),
            "created_at": product.get("created_at").isoformat() if product.get("created_at") else None
        }