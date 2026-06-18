
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab-btn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

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

    
    tabs.forEach(function(btn) {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    
    document.getElementById('loginForm').addEventListener('submit', function(e) {
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
        alert('✅ Вход выполнен! (демо)');
    });

    
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('regEmail').value.trim();
        const password = document.getElementById('regPassword').value.trim();
        const confirm = document.getElementById('regConfirmPassword').value.trim();
        const errorEl = document.getElementById('registerError');

        if (!email || !password || !confirm) {
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
        alert('✅ Регистрация выполнена! (демо)');
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