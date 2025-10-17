// ==================== CONFIGURACIÓN ====================
const API_URL = 'http://localhost:5000/api';

// ==================== UTILIDADES DE AUTENTICACIÓN ====================

// Obtener el token del localStorage
const getToken = () => {
    return localStorage.getItem('token');
};

// Guardar el token
const saveToken = (token) => {
    localStorage.setItem('token', token);
};

// Guardar datos del usuario
const saveUser = (user) => {
    localStorage.setItem('user', JSON.stringify(user));
};

// Obtener datos del usuario
const getUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

// Limpiar autenticación y redirigir
const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
};

// Verificar si el usuario está autenticado
const isAuthenticated = () => {
    return getToken() !== null;
};

// ==================== AUTENTICACIÓN ====================

// Registrar usuario
async function register(userData) {
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            saveToken(data.data.token);
            saveUser(data.data.user);
        }
        
        return data;
    } catch (error) {
        console.error('Error en registro:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Login de usuario
async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            saveToken(data.data.token);
            saveUser(data.data.user);
        }
        
        return data;
    } catch (error) {
        console.error('Error en login:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// ==================== PRODUCTOS ====================

// Obtener todos los productos
async function getProducts(page = 1, limit = 20, filters = {}) {
    try {
        const params = new URLSearchParams({
            page: page.toString(),
            limit: limit.toString(),
            ...filters
        });
        
        const response = await fetch(`${API_URL}/products/?${params}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al obtener productos:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Obtener un producto específico
async function getProduct(productId) {
    try {
        const response = await fetch(`${API_URL}/products/${productId}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al obtener producto:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Crear un producto (requiere autenticación)
async function createProduct(formData) {
    try {
        const token = getToken();
        
        if (!token) {
            return { success: false, message: 'Debes iniciar sesión para publicar' };
        }
        
        const response = await fetch(`${API_URL}/products/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData // FormData con imagen
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al crear producto:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Actualizar un producto
async function updateProduct(productId, formData) {
    try {
        const token = getToken();
        
        if (!token) {
            return { success: false, message: 'Debes iniciar sesión' };
        }
        
        const response = await fetch(`${API_URL}/products/${productId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al actualizar producto:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Eliminar un producto
async function deleteProduct(productId) {
    try {
        const token = getToken();
        
        if (!token) {
            return { success: false, message: 'Debes iniciar sesión' };
        }
        
        const response = await fetch(`${API_URL}/products/${productId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al eliminar producto:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Buscar productos
async function searchProducts(query, page = 1) {
    try {
        const params = new URLSearchParams({
            search: query,
            page: page.toString()
        });
        
        const response = await fetch(`${API_URL}/products/?${params}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al buscar productos:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Filtrar productos por categoría
async function filterByCategory(categoria, page = 1) {
    try {
        const params = new URLSearchParams({
            categoria: categoria,
            page: page.toString()
        });
        
        const response = await fetch(`${API_URL}/products/?${params}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al filtrar productos:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Obtener categorías disponibles
async function getCategories() {
    try {
        const response = await fetch(`${API_URL}/products/categories`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al obtener categorías:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Obtener productos de un usuario
async function getUserProducts(userId, page = 1) {
    try {
        const params = new URLSearchParams({
            page: page.toString()
        });
        
        const response = await fetch(`${API_URL}/products/user/${userId}?${params}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al obtener productos del usuario:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// ==================== USUARIOS ====================

// Obtener mi perfil
async function getMyProfile() {
    try {
        const token = getToken();
        
        if (!token) {
            return { success: false, message: 'Debes iniciar sesión' };
        }
        
        const response = await fetch(`${API_URL}/users/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error al obtener perfil:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Actualizar mi perfil
async function updateMyProfile(userData) {
    try {
        const token = getToken();
        
        if (!token) {
            return { success: false, message: 'Debes iniciar sesión' };
        }
        
        const response = await fetch(`${API_URL}/users/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            saveUser(data.data); // Actualizar datos en localStorage
        }
        
        return data;
    } catch (error) {
        console.error('Error al actualizar perfil:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// Obtener perfil público de un usuario
async function getUserProfile(userId) {
    try {
        const response = await fetch(`${API_URL}/users/${userId}`);
        const data = await response.json();
        
        return data;
    } catch (error) {
        console.error('Error al obtener usuario:', error);
        return { success: false, message: 'Error de conexión con el servidor' };
    }
}

// ==================== UTILIDADES DE UI ====================

// Mostrar mensajes de alerta
function showAlert(message, type = 'info') {
    // Crear elemento de alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Verificar autenticación en páginas protegidas
function requireAuth() {
    if (!isAuthenticated()) {
        showAlert('Debes iniciar sesión para acceder a esta página', 'warning');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        return false;
    }
    return true;
}

// Actualizar navbar con datos del usuario
function updateNavbar() {
    const user = getUser();
    const navbarNav = document.querySelector('#navbarNav .navbar-nav');
    
    if (user && navbarNav) {
        // Buscar el item de "Perfil" y actualizarlo
        const perfilLink = navbarNav.querySelector('a[href="perfil.html"]');
        if (perfilLink) {
            perfilLink.textContent = `Perfil (${user.username})`;
        }
        
        // Agregar botón de logout si no existe
        if (!document.getElementById('logoutBtn')) {
            const logoutItem = document.createElement('li');
            logoutItem.className = 'nav-item';
            logoutItem.innerHTML = `
                <a class="nav-link text-danger" href="#" id="logoutBtn">
                    <i class="bi bi-box-arrow-right"></i> Salir
                </a>
            `;
            navbarNav.appendChild(logoutItem);
            
            document.getElementById('logoutBtn').addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
                    logout();
                }
            });
        }
    }
}