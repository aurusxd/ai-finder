const API_BASE_URL = 'http://localhost:8000';
const AUTH_STORAGE_KEY = 'ai_finder_auth';

function saveAuth(data) {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(data));
}

function getAuth() {
    const raw = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!raw) {
        return null;
    }

    try {
        return JSON.parse(raw);
    } catch {
        return null;
    }
}

function clearAuth() {
    localStorage.removeItem(AUTH_STORAGE_KEY);
}

function requireAuth() {
    if (!getAuth()) {
        window.location.href = 'registration-view.html';
    }
}

async function parseErrorResponse(response) {
    try {
        const data = await response.json();
        if (typeof data.detail === 'string') {
            return data.detail;
        }
        if (Array.isArray(data.detail)) {
            return data.detail.map(function(item) {
                return item.msg || String(item);
            }).join(', ');
        }
    } catch {
        // ignore parse errors
    }

    return 'Произошла ошибка. Попробуйте снова.';
}
