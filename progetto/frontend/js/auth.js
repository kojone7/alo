// Configurazione base per le chiamate API
const API_BASE_URL = 'http://localhost:8081';

// Funzioni di autenticazione e gestione utenti
document.addEventListener('DOMContentLoaded', function() {
    // Controlla se l'utente è già loggato
    checkAuthStatus();

    // Gestione del form di login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            login();
        });
    }

    // Gestione del form di registrazione
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            register();
        });
    }

    // Gestione del logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }

    // Aggiorna la navigazione al caricamento della pagina
    updateNavigation();
});

// Controlla lo stato di autenticazione
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user'));

    // Se siamo in una pagina protetta e non c'è token, redirect al login
    if (!token && isProtectedPage()) {
        window.location.href = 'login.html';
        return;
    }

    // Se siamo nel login/register e c'è già un token, redirect alla dashboard
    if (token && (isLoginPage() || isRegisterPage())) {
        window.location.href = 'dashboard.html';
        return;
    }

    // Se siamo in una pagina protetta, aggiorna l'interfaccia con i dati utente
    if (token && user && isProtectedPage()) {
        updateUserInterface(user);
    }
}

// Funzione di login
async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('loginError');

    try {
        const response = await fetch('/api/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
        });

        if (!response.ok) {
            throw new Error('Email o password non corretti');
        }

        const data = await response.json();

        // Salva token e dati utente
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify({
            id: data.user_id,
            email: email
        }));

        // Redirect alla dashboard
        window.location.href = 'dashboard.html';
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.style.display = 'block';
    }
}

// Funzione di registrazione
async function register() {
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const address = document.getElementById('address').value;
    const city = document.getElementById('city').value;
    const cap = document.getElementById('cap').value;
    const phone = document.getElementById('phone').value;
    
    // Validazione base
    if (!fullName || !email || !password || !confirmPassword || !address || !city || !cap || !phone) {
        showError('Compila tutti i campi obbligatori');
        return;
    }

    if (password !== confirmPassword) {
        showError('Le password non coincidono');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                full_name: fullName,
                password: password,
                address: address,
                city: city,
                cap: cap,
                phone: phone
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore durante la registrazione');
        }

        const data = await response.json();

        // Effettua il login automatico dopo la registrazione
        const loginResponse = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
        });

        if (!loginResponse.ok) {
            throw new Error('Errore durante il login automatico');
        }

        const loginData = await loginResponse.json();

        // Salva token e dati utente
        localStorage.setItem('token', loginData.access_token);
        localStorage.setItem('user', JSON.stringify({
            id: loginData.user_id,
            email: email,
            full_name: fullName
        }));

        // Aggiorna l'interfaccia
        updateNavigation();

        // Redirect alla dashboard
        window.location.href = 'dashboard.html';
    } catch (error) {
        showError(error.message);
    }
}

// Funzione per mostrare errori
function showError(message) {
    const errorElement = document.querySelector('.error-message') || document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.style.color = 'red';
    errorElement.style.marginBottom = '1rem';
    
    const form = document.querySelector('form');
    if (!document.querySelector('.error-message')) {
        form.insertBefore(errorElement, form.firstChild);
    }
}

// Funzione per aggiornare la navigazione
function updateNavigation() {
    const navLinks = document.querySelector('.nav-links');
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user'));

    if (token && user) {
        // Utente autenticato
        navLinks.innerHTML = `
            <li><a href="dashboard.html">Dashboard</a></li>
            <li><a href="#" class="btn btn-outline" id="logoutBtn">Logout</a></li>
        `;
        
        // Aggiungi event listener per il logout
        document.getElementById('logoutBtn').addEventListener('click', logout);
    } else {
        // Utente non autenticato
        navLinks.innerHTML = `
            <li><a href="index.html#features">Funzionalità</a></li>
            <li><a href="index.html#how-it-works">Come Funziona</a></li>
            <li><a href="index.html#stats">Statistiche</a></li>
            <li><a href="login.html" class="btn btn-outline">Accedi</a></li>
            <li><a href="register.html" class="btn btn-primary">Registrati</a></li>
        `;
    }
}

// Funzione di logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Funzioni di utilità
function isProtectedPage() {
    return window.location.pathname.includes('dashboard.html') ||
           window.location.pathname.includes('profile.html');
}

function isLoginPage() {
    return window.location.pathname.includes('login.html');
}

function isRegisterPage() {
    return window.location.pathname.includes('register.html');
}

function updateUserInterface(user) {
    // Aggiorna l'interfaccia utente con i dati dell'utente loggato
    const userNameElement = document.getElementById('userName');
    if (userNameElement) {
        userNameElement.textContent = user.email;
    }
}

// Funzione per gestire la registrazione
async function handleRegistration(event) {
    event.preventDefault();
    
    try {
        // Validazione base
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (password !== confirmPassword) {
            throw new Error('Le password non coincidono');
        }

        // Raccogli i dati dal form
        const formData = {
            email: document.getElementById('email').value,
            full_name: document.getElementById('fullName').value,
            password: password,
            confirm_password: confirmPassword
        };

        console.log('Invio dati registrazione:', formData);

        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        console.log('Risposta server:', response);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Errore durante la registrazione');
        }

        const data = await response.json();
        console.log('Registrazione completata:', data);
        
        alert('Registrazione completata con successo! Ora puoi effettuare il login.');
        window.location.href = 'login.html';
    } catch (error) {
        console.error('Errore durante la registrazione:', error);
        const errorMsg = document.getElementById('registerError');
        if (errorMsg) {
            errorMsg.textContent = error.message || 'Si è verificato un errore durante la registrazione';
            errorMsg.style.display = 'block';
        }
    }
}

// Funzione per gestire il login
async function handleLogin(event) {
    event.preventDefault();
    
    try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        console.log('Tentativo di login per:', email);

        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Credenziali non valide');
        }

        const data = await response.json();
        console.log('Login completato:', data);

        // Salva token e dati utente
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify({
            id: data.user_id,
            email: email
        }));

        // Aggiorna l'interfaccia
        updateNavigation();
        
        // Redirect alla dashboard
        window.location.href = 'dashboard.html';
    } catch (error) {
        console.error('Errore durante il login:', error);
        const errorMsg = document.getElementById('loginError');
        if (errorMsg) {
            errorMsg.textContent = error.message || 'Si è verificato un errore durante il login';
            errorMsg.style.display = 'block';
        }
    }
}

// Aggiungi gli event listener quando il DOM è caricato
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM caricato, inizializzazione event listeners');
    
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    if (registerForm) {
        console.log('Form di registrazione trovato');
        registerForm.addEventListener('submit', handleRegistration);
    }

    if (loginForm) {
        console.log('Form di login trovato');
        loginForm.addEventListener('submit', handleLogin);
    }

    // Gestione toggle password
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });
});

// Funzione per verificare se l'utente è autenticato
function isAuthenticated() {
    return localStorage.getItem('token') !== null;
}