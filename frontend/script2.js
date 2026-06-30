requireAuth();

const auth = getAuth();
if (auth && auth.user) {
    document.getElementById('profileName').textContent = auth.user.username;
    document.getElementById('profileEmail').textContent = auth.user.email_address;
}

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
const profileMenuBtn = document.getElementById('profileMenuBtn');
const profileDropdown = document.getElementById('profileDropdown');
const logoutBtn = document.getElementById('logoutBtn');
const fileInput = document.getElementById('fileInput');
const selectedFilePreview = document.getElementById('selectedFilePreview');
const chatHistoryList = document.getElementById('chatHistoryList');
const chatTitle = document.querySelector('.chat-header h2');

let selectedFile = null;
let currentChatId = null;
let chatHistory = [];

function getMessageTime(value) {
    const currentTime = value ? new Date(value) : new Date();
    const hours = String(currentTime.getHours()).padStart(2, '0');
    const minutes = String(currentTime.getMinutes()).padStart(2, '0');

    return hours + ':' + minutes;
}

function getChatTitle(chat) {
    return 'Чат #' + chat.id;
}

function formatChatDate(value) {
    if (!value) {
        return '';
    }

    return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
    }).format(new Date(value));
}

function formatFileSize(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) {
        return 'Размер неизвестен';
    }

    const units = ['Б', 'КБ', 'МБ', 'ГБ'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex += 1;
    }

    const formattedSize = size >= 10 || unitIndex === 0
        ? Math.round(size)
        : size.toFixed(1);

    return formattedSize + ' ' + units[unitIndex];
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function setChatTitle(title) {
    chatTitle.innerHTML = '';

    const icon = document.createElement('i');
    icon.className = 'fas fa-comment-dots';
    icon.style.marginRight = '10px';
    icon.style.color = '#1a73e8';

    chatTitle.appendChild(icon);
    chatTitle.appendChild(document.createTextNode(title));
}

function setChatViewActive() {
    startScreen.classList.add('hidden');
    messagesArea.classList.remove('hidden');
    chatInputArea.classList.add('active');
}

function setStartViewActive() {
    startScreen.classList.remove('hidden');
    messagesArea.classList.add('hidden');
    chatInputArea.classList.remove('active');
    messagesArea.innerHTML = '';
    currentChatId = null;
    setChatTitle('Новый чат');
    renderChatHistory();
}

function renderChatHistory() {
    chatHistoryList.innerHTML = '';

    if (!chatHistory.length) {
        const empty = document.createElement('div');
        empty.className = 'chat-history-empty';
        empty.textContent = 'Чатов пока нет';
        chatHistoryList.appendChild(empty);
        return;
    }

    chatHistory.forEach(function(chat) {
        const item = document.createElement('button');
        item.className = 'chat-history-item';
        item.type = 'button';
        item.dataset.chatId = chat.id;

        if (chat.id === currentChatId) {
            item.classList.add('active');
        }

        const name = document.createElement('span');
        name.className = 'chat-history-name';
        name.textContent = getChatTitle(chat);

        const date = document.createElement('span');
        date.className = 'chat-history-date';
        date.textContent = formatChatDate(chat.created_at);

        item.appendChild(name);
        item.appendChild(date);
        item.addEventListener('click', function() {
            loadChat(chat.id);
        });

        chatHistoryList.appendChild(item);
    });
}

async function loadChatHistory() {
    try {
        const response = await fetch(API_BASE_URL + '/chats/user/' + auth.user.id, {
            credentials: 'include',
        });

        if (!response.ok) {
            console.error('Не удалось загрузить историю чатов', response);
            return;
        }

        chatHistory = await response.json();
        renderChatHistory();
    } catch (error) {
        console.error('Ошибка загрузки истории чатов:', error);
    }
}

async function createChat() {
    const response = await fetch(API_BASE_URL + '/chats/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            user_id: auth.user.id,
            created_at: new Date().toISOString(),
        }),
    });

    if (!response.ok) {
        throw new Error('Не удалось создать чат');
    }

    const chat = await response.json();
    currentChatId = chat.id;
    setChatTitle(getChatTitle(chat));
    await loadChatHistory();
    return chat;
}

function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message gpt loading-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar gpt';
    avatar.textContent = 'G';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    const loader = document.createElement('div');
    loader.className = 'message-loader';
    loader.setAttribute('aria-label', 'AI думает');

    const spinner = document.createElement('span');
    spinner.className = 'message-spinner';

    const text = document.createElement('span');
    text.textContent = '';

    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = getMessageTime();

    loader.appendChild(spinner);
    loader.appendChild(text);
    bubble.appendChild(loader);
    bubble.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;

    return messageDiv;
}

function renderMessage(text, isUser = false, createdAt = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'gpt'}`;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${isUser ? 'user' : 'gpt'}`;
    avatar.textContent = isUser ? 'Вы' : 'G';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';

    const p = document.createElement('p');
    p.textContent = text;

    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = getMessageTime(createdAt);

    bubble.appendChild(p);
    bubble.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

async function addMessage(text, isUser = false) {
    renderMessage(text, isUser);

    if (!currentChatId) {
        return;
    }

    try {
        const response = await fetch(API_BASE_URL + '/messages/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                content: text,
                role: isUser ? 'user' : 'gpt',
                created_at: new Date().toISOString(),
                chat_id: currentChatId,
            }),
        });

        if (!response.ok) {
            console.error('Ошибка выполнения запроса', response);
        }
    } catch (error) {
        console.error(error);
    }
}

async function openChat(query) {
    setChatViewActive();
    messagesArea.innerHTML = '';

    try {
        await createChat();
        await handleChatSend(query);
    } catch (error) {
        console.error(error);
    }

    chatInput.value = '';
    chatInput.focus();
}

async function loadChat(chatId) {
    currentChatId = Number(chatId);
    setChatViewActive();
    messagesArea.innerHTML = '';

    const chat = chatHistory.find(function(item) {
        return item.id === currentChatId;
    });

    setChatTitle(chat ? getChatTitle(chat) : 'Чат');
    renderChatHistory();

    try {
        const response = await fetch(API_BASE_URL + '/messages/chat/' + currentChatId, {
            credentials: 'include',
        });

        if (!response.ok) {
            console.error('Не удалось загрузить сообщения чата', response);
            return;
        }

        const messages = await response.json();
        messagesArea.innerHTML = '';

        messages.forEach(function(message) {
            renderMessage(message.content, message.role === 'user', message.created_at);
        });

        chatInput.value = '';
        chatInput.focus();
    } catch (error) {
        console.error('Ошибка загрузки сообщений чата:', error);
    }
}

function handleStartSend() {
    const query = startInput.value.trim();
    if (query) {
        openChat(query);
    }
}

startSendBtn.addEventListener('click', function(e) {
    e.preventDefault();
    handleStartSend();
});

startInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleStartSend();
    }
});

startAttachBtn.addEventListener('click', function() {
    fileInput.click();
});

async function handleChatSend(query) {
    let loadingMessage = null;

    try {
        const formData = new FormData();
        const messageText =
            typeof query === 'string' ? query.trim() : chatInput.value.trim();

        if (!messageText) {
            return;
        }

        if (!currentChatId) {
            await createChat();
        }

        formData.append('question', messageText);
        formData.append('user_id', auth.user.id);

        if (selectedFile) {
            formData.append('file', selectedFile);
        }

        await addMessage(messageText, true);
        chatInput.value = '';
        loadingMessage = addLoadingMessage();

        const response = await fetch(API_BASE_URL + '/ai/ask', {
            method: 'POST',
            credentials: 'include',
            body: formData,
        });

        if (!response.ok) {
            console.error(await response.text());
            loadingMessage.remove();
            return;
        }

        const data = await response.json();
        loadingMessage.remove();
        await addMessage(data.answer, false);
        await loadChatHistory();
    } catch (error) {
        if (loadingMessage) {
            loadingMessage.remove();
        }
        console.error('Ошибка при отправке сообщения: ', error);
    }
}

chatSendBtn.addEventListener('click', function(e) {
    e.preventDefault();
    handleChatSend();
});

chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        handleChatSend();
    }
});

attachBtn.addEventListener('click', function() {
    fileInput.click();
});

newChatBtn.addEventListener('click', function() {
    setStartViewActive();
    startInput.value = '';
    startInput.focus();
});

profileMenuBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    profileDropdown.classList.toggle('active');
});

document.addEventListener('click', function(e) {
    if (!profileMenuBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('active');
    }
});

logoutBtn.addEventListener('click', function() {
    window.location.href = 'registration-view.html';
    localStorage.clear();
    profileDropdown.classList.remove('active');
});

fileInput.addEventListener('change', function(e) {
    selectedFile = e.target.files[0];

    if (!selectedFile) {
        return;
    }

    selectedFilePreview.classList.remove('hidden');
    selectedFilePreview.innerHTML = `
        <div class="file-preview-icon" aria-hidden="true">📄</div>
        <div class="file-preview-info">
            <span class="file-preview-name">${escapeHtml(selectedFile.name)}</span>
            <span class="file-preview-meta">${formatFileSize(selectedFile.size)}</span>
        </div>
        <button class="file-remove-btn" type="button" id="removeFileBtn" aria-label="Убрать файл">×</button>
    `;

    document.getElementById('removeFileBtn').addEventListener('click', function() {
        selectedFile = null;
        fileInput.value = '';
        selectedFilePreview.classList.add('hidden');
        selectedFilePreview.innerHTML = '';
    });
});

loadChatHistory();
startInput.focus();
