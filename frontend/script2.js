
const startScreen = document.getElementById('startScreen');
const messagesArea = document.getElementById('messagesArea');
const chatInputArea = document.getElementById('chatInputArea');
const startInput = document.getElementById('startInput');
const startSendBtn = document.getElementById('startSendBtn');
const startAttachBtn = document.getElementById('startAttachBtn');
const chatInput = document.getElementById('chatInput');
const chatSendBtn = document.getElementById('chatSendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const attachBtn = document.getElementById('attachBtn');


function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'gpt'}`;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${isUser ? 'user' : 'gpt'}`;
    avatar.textContent = isUser ? '👤' : 'G';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    const p = document.createElement('p');
    p.textContent = text;

    const time = document.createElement('div');
    time.className = 'message-time';
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    time.textContent = hours + ':' + minutes;

    bubble.appendChild(p);
    bubble.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}


function openChat(query) {
    startScreen.classList.add('hidden');
    messagesArea.classList.remove('hidden');
    chatInputArea.classList.add('active');

    messagesArea.innerHTML = '';
    addMessage('Привет! Чем могу помочь? 😊', false);

    if (query && query.trim()) {
        addMessage(query.trim(), true);
        setTimeout(function() {
            addMessage('Спасибо за ваш вопрос! Я обрабатываю запрос: "' + query.trim() + '". Чем ещё могу помочь?', false);
        }, 500);
    }

    chatInput.value = '';
    chatInput.focus();
}


function handleStartSend() {
    const query = startInput.value.trim();
    if (query) {
        openChat(query);
    }
}

startSendBtn.addEventListener('click', handleStartSend);
startInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleStartSend();
    }
});


startAttachBtn.addEventListener('click', function() {
    alert('Функция прикрепления документов (демо)');
});


function handleChatSend() {
    const query = chatInput.value.trim();
    if (query) {
        addMessage(query, true);
        chatInput.value = '';

        setTimeout(function() {
            const responses = [
                'Отличный вопрос! Давайте разберёмся.',
                'Интересно! Расскажите подробнее.',
                'Я понимаю. Вот что я думаю по этому поводу.',
                'Спасибо за уточнение! Продолжим.',
                'Хорошо, я запомнил. Что дальше?'
            ];
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addMessage(randomResponse, false);
        }, 600);
    }
}

chatSendBtn.addEventListener('click', handleChatSend);
chatInput.addEventListener('keydown', function(e) {ы
    if (e.key === 'Enter') {
        e.preventDefault();
        handleChatSend();
    }
});


attachBtn.addEventListener('click', function() {
    alert('Функция прикрепления документов (демо)');
});


newChatBtn.addEventListener('click', function() {
    startScreen.classList.remove('hidden');
    messagesArea.classList.add('hidden');
    chatInputArea.classList.remove('active');
    startInput.value = '';
    startInput.focus();
});


startInput.focus();