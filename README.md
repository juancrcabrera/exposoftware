# 🌱 TRADEco - Plataforma de Moda Circular & Trueques

TRADEco es una plataforma web completa para la compra, venta e intercambio de ropa de segunda mano. Promueve la economía circular y la moda sostenible, permitiendo a los usuarios dar nueva vida a sus prendas mientras obtienen beneficios.

## ✨ Características

### Para Usuarios
- 👕 **Publicación de Productos**: Sube fotos, descripciones y precios de tus prendas
- 🔍 **Búsqueda y Filtros**: Encuentra productos por categoría, precio o búsqueda por texto
- 👤 **Perfil de Usuario**: Gestiona tu información personal y tus publicaciones
- 🎁 **Sistema de Beneficios**: Obtén descuentos y recompensas por participar
- 📱 **Interfaz Responsive**: Diseño adaptable para móviles, tablets y escritorio

### Para Administradores
- 📊 **Dashboard Completo**: Estadísticas en tiempo real de usuarios y productos
- 📈 **Gráficos Interactivos**: Visualización de datos con Chart.js
- 👥 **Gestión de Usuarios**: Visualiza y administra la base de usuarios
- 📦 **Control de Productos**: Monitorea productos publicados y su estado

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0**: Framework web de Python
- **MongoDB**: Base de datos NoSQL
- **PyJWT**: Autenticación con JSON Web Tokens
- **Bcrypt**: Encriptación de contraseñas
- **Flask-CORS**: Manejo de CORS para API REST
- **Pillow**: Procesamiento de imágenes

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **Bootstrap 5.3**: Framework CSS responsive
- **Vanilla JavaScript**: Lógica del cliente sin frameworks pesados
- **Chart.js**: Visualización de datos en el dashboard
- **Bootstrap Icons**: Iconografía moderna

### Base de Datos
- **MongoDB 7.0**: Base de datos principal
- **Mongo Express**: Interfaz web para administración de BD (opcional)

## 📋 Requisitos Previos

- Python 3.8 o superior
- Docker y Docker Compose (para MongoDB)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/tradeco.git
cd tradeco
```

### 2. Iniciar MongoDB con Docker

```bash
docker-compose up -d
```

Esto iniciará:
- MongoDB en `localhost:27017`
- Mongo Express en `localhost:8081` (interfaz web)

### 3. Configurar el Backend

```bash
cd backend
```

Crear entorno virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Crear carpeta de uploads:
```bash
mkdir -p ../uploads/products
```

### 4. Configurar Variables de Entorno

El archivo `.env` ya está configurado con valores por defecto. Asegúrate de cambiar el `JWT_SECRET_KEY` en producción:

```env
MONGODB_URI=mongodb://admin:admin123@localhost:27017/
DB_NAME=tradeco_db
JWT_SECRET_KEY=tu_clave_secreta_super_segura_cambiala
JWT_EXPIRATION_HOURS=24
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
UPLOAD_FOLDER=../uploads/products
MAX_FILE_SIZE=5242880
```

### 5. Crear Usuario Administrador

```bash
python create_admin.py
```

Credenciales del admin:
- **Email**: admin@tradeco.com
- **Password**: Admin123

### 6. Iniciar el Servidor Backend

```bash
python app.py
```

El servidor estará corriendo en `http://localhost:5000`

### 7. Acceder al Frontend

Abre tu navegador en `http://localhost:5000` o directamente abre el archivo `frontend/index.html` en tu navegador.

## 📁 Estructura del Proyecto

```
tradeco/
├── backend/
│   ├── app.py                 # Aplicación principal Flask
│   ├── config.py              # Configuración y variables de entorno
│   ├── requirements.txt       # Dependencias de Python
│   ├── create_admin.py        # Script para crear admin
│   ├── models/
│   │   ├── user.py           # Modelo de Usuario
│   │   └── product.py        # Modelo de Producto
│   ├── routes/
│   │   ├── auth.py           # Rutas de autenticación
│   │   ├── products.py       # Rutas de productos
│   │   ├── users.py          # Rutas de usuarios
│   │   └── dashboard.py      # Rutas del dashboard
│   ├── middleware/
│   │   └── auth_middleware.py # Middleware de autenticación
│   └── utils/
│       └── validators.py     # Validadores de datos
├── frontend/
│   ├── index.html            # Página principal
│   ├── login.html            # Página de login/registro
│   ├── publicar.html         # Formulario de publicación
│   ├── perfil.html           # Página de perfil de usuario
│   ├── beneficios.html       # Página de beneficios
│   ├── dashboard.html        # Dashboard administrativo
│   ├── api.js                # Cliente API JavaScript
│   └── styles.css            # Estilos personalizados
├── uploads/
│   └── products/             # Imágenes de productos subidas
├── docker-compose.yml        # Configuración de Docker
└── mongo-init.js            # Script de inicialización de MongoDB
```

## 🔐 Autenticación y Autorización

El sistema utiliza JWT (JSON Web Tokens) para la autenticación:

1. **Registro/Login**: El usuario se registra o inicia sesión
2. **Token JWT**: Se genera un token con duración de 24 horas
3. **Almacenamiento**: El token se guarda en `localStorage` del navegador
4. **Autorización**: El token se envía en el header `Authorization: Bearer <token>`

### Roles de Usuario

- **usuario**: Puede publicar, editar y eliminar sus propios productos
- **admin**: Acceso total, incluido el dashboard y gestión de todos los usuarios/productos

## 📡 API Endpoints

### Autenticación
```
POST /api/auth/register      - Registrar nuevo usuario
POST /api/auth/login         - Iniciar sesión
```

### Productos
```
GET    /api/products/                    - Obtener todos los productos
GET    /api/products/<id>                - Obtener un producto específico
POST   /api/products/                    - Crear producto (requiere auth)
PUT    /api/products/<id>                - Actualizar producto (requiere auth)
DELETE /api/products/<id>                - Eliminar producto (requiere auth)
GET    /api/products/categories          - Obtener categorías
GET    /api/products/user/<user_id>      - Productos de un usuario
```

### Usuarios
```
GET    /api/users/profile    - Obtener mi perfil (requiere auth)
PUT    /api/users/profile    - Actualizar mi perfil (requiere auth)
GET    /api/users/<id>       - Obtener perfil público de usuario
GET    /api/users/           - Obtener todos los usuarios (solo admin)
```

### Dashboard (Solo Admin)
```
GET    /api/dashboard/stats                  - Estadísticas generales
GET    /api/dashboard/products-by-category   - Productos por categoría
GET    /api/dashboard/recent-activity        - Actividad reciente
GET    /api/dashboard/users-growth           - Crecimiento de usuarios
GET    /api/dashboard/top-sellers            - Top vendedores
GET    /api/dashboard/price-stats            - Estadísticas de precios
```

## 🎨 Categorías de Productos

- 👕 Remeras
- 🧥 Abrigos
- 👖 Pantalones
- 👗 Vestidos
- 👟 Calzado
- 🎒 Accesorios

## 🔒 Seguridad

- **Contraseñas**: Hasheadas con bcrypt (salt rounds)
- **JWT**: Tokens firmados con clave secreta
- **Validaciones**: Email, teléfono, username y contraseña validados en backend
- **CORS**: Configurado para permitir peticiones desde el frontend
- **Archivos**: Solo se permiten imágenes (JPG, PNG, GIF, WEBP) hasta 5MB

## 🐛 Solución de Problemas

### Error de conexión a MongoDB

```bash
# Verificar que los contenedores estén corriendo
docker ps

# Si no están corriendo, iniciarlos
docker-compose up -d
```

### Error al subir imágenes

```bash
# Verificar que la carpeta de uploads existe
mkdir -p uploads/products

# Verificar permisos (Linux/Mac)
chmod 755 uploads/products
```

### Error 401 (No autorizado)

- Verifica que el token esté presente en `localStorage`
- El token puede haber expirado (24 horas)
- Intenta cerrar sesión e iniciar sesión nuevamente

### Backend no inicia

```bash
# Verificar que todas las dependencias estén instaladas
pip install -r requirements.txt

# Verificar que MongoDB esté corriendo
docker-compose ps

# Ver logs del backend
python app.py
```

## 📝 Validaciones

### Contraseña
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos una letra minúscula
- Al menos un número

### Username
- Entre 3 y 20 caracteres
- Solo letras, números y guiones bajos

### Email
- Formato válido de email

### Teléfono (opcional)
- Formato argentino: +54 o 0 seguido de 10-11 dígitos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- Juan Cruz Cabrera
- Santino Thomas Rodas

## 🙏 Agradecimientos

- Bootstrap por el framework CSS
- Chart.js por las visualizaciones de datos
- MongoDB por la base de datos
- Flask por el framework web
- La comunidad de código abierto

## 📞 Contacto

- Email: contacto@tradeco.com
- GitHub: [https://github.com/tu-usuario/tradeco](https://github.com/tu-usuario/tradeco)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!

🌱 **TRADEco** - Moda Circular & Trueques
