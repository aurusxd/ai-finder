
document.addEventListener('DOMContentLoaded', function() {
    if (getAuth()) {
        window.location.href = 'index.html';
        return;
    }

    const tabs = document.querySelectorAll('.tab-btn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginSubmitBtn = loginForm.querySelector('.btn');
    const registerSubmitBtn = registerForm.querySelector('.btn');

    function switchTab(tabName) {
        tabs.forEach(function(btn) {
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        if (tabName === 'login') {
            loginForm.classList.add('active');
            registerForm.classList.remove('active');
        } else {
            registerForm.classList.add('active');
            loginForm.classList.remove('active');
        }

        document.getElementById('loginError').textContent = '';
        document.getElementById('registerError').textContent = '';
    }

    function setLoading(button, isLoading, defaultText) {
        button.disabled = isLoading;
        button.textContent = isLoading ? 'Загрузка...' : defaultText;
    }

    tabs.forEach(function(btn) {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value.trim();
        const errorEl = document.getElementById('loginError');

        if (!email || !password) {
            errorEl.textContent = '⚠️ Заполните все поля';
            return;
        }

        if (!email.includes('@')) {
            errorEl.textContent = '⚠️ Введите корректный email';
            return;
        }

        errorEl.textContent = '';
        setLoading(loginSubmitBtn, true, 'Войти');

        try {
            const response = await fetch(API_BASE_URL + '/users/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: email,
                    password: password,
                }),
            });

            if (!response.ok) {
                errorEl.textContent = '⚠️ ' + await parseErrorResponse(response);
                return;
            }

            const data = await response.json();
            saveAuth(data);
            window.location.href = 'index.html';
        } catch {
            errorEl.textContent = '⚠️ Не удалось подключиться к серверу';
        } finally {
            setLoading(loginSubmitBtn, false, 'Войти');
        }
    });

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const name = document.getElementById('regName').value.trim();
        const email = document.getElementById('regEmail').value.trim();
        const password = document.getElementById('regPassword').value.trim();
        const confirm = document.getElementById('regConfirmPassword').value.trim();
        const errorEl = document.getElementById('registerError');

        if (!name || !email || !password || !confirm) {
            errorEl.textContent = '⚠️ Заполните все поля';
            return;
        }

        if (!email.includes('@')) {
            errorEl.textContent = '⚠️ Введите корректный email';
            return;
        }

        if (password.length < 6) {
            errorEl.textContent = '⚠️ Пароль должен быть минимум 6 символов';
            return;
        }

        if (password !== confirm) {
            errorEl.textContent = '⚠️ Пароли не совпадают';
            return;
        }

        errorEl.textContent = '';
        setLoading(registerSubmitBtn, true, 'Зарегистрироваться');

        try {
            const response = await fetch(API_BASE_URL + '/users/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: name,
                    email_address: email,
                    password: password,
                }),
            });

            if (!response.ok) {
                errorEl.textContent = '⚠️ ' + await parseErrorResponse(response);
                return;
            }

            const data = await response.json();
            saveAuth(data);
            window.location.href = 'index.html';
        } catch {
            errorEl.textContent = '⚠️ Не удалось подключиться к серверу';
        } finally {
            setLoading(registerSubmitBtn, false, 'Зарегистрироваться');
        }
    });

    document.querySelectorAll('.footer-text a').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tab = this.getAttribute('onclick');
            if (tab) {
                const match = tab.match(/switchTab\('([^']+)'\)/);
                if (match) {
                    switchTab(match[1]);
                }
            }
        });
    });

    window.switchTab = switchTab;
});
