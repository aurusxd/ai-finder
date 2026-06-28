
requireAuth();

const auth = getAuth();
console.log(auth);
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
const now = new Date();
const profileMenuBtn = document.getElementById('profileMenuBtn');
const profileDropdown = document.getElementById('profileDropdown');
const logoutBtn = document.getElementById('logoutBtn');
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("attachBtn");
const selectedFilePreview = document.getElementById('selectedFilePreview');

let selectedFile = null;

async function addMessage(text, isUser = false) {
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
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    time.textContent = hours + ':' + minutes;

    bubble.appendChild(p);
    bubble.appendChild(time);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);

    messagesArea.appendChild(messageDiv);
    messagesArea.scrollTop = messagesArea.scrollHeight;
        try {
            const response = await fetch(API_BASE_URL + '/messages/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    content: text,
                    role:  isUser ? 'user' : 'gpt',
                    created_at: now,
                    chat_id: 1
                }),
            });
            if(!response.ok){
                console.error("Ошибка выполнения запроса",response)
            }
        } catch (error){
            console.error(error);
        }
}


async function openChat(query) {

    startScreen.classList.add('hidden');
    messagesArea.classList.remove('hidden');
    chatInputArea.classList.add('active');

    messagesArea.innerHTML = '';

            try {
            const user = getAuth();
            console.log(user)
            const response = await fetch(API_BASE_URL + '/chats/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    user_id: user.user.id,
                    created_at: now,
      
                }),
            });
            if(!response.ok){
                console.error("Ошибка выполнения запроса: ",response)
            }
            console.log(response);
            } catch (error){
                console.error(error);
            }

    handleChatSend(query);

    

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
    fileInput.click();

});


async function handleChatSend(query) {
        const messageText = typeof query === 'string' ? query.trim() : chatInput.value.trim();
        if (messageText) {
        addMessage(messageText, true);
        chatInput.value = '';
                try {
                    const response = await fetch(API_BASE_URL + '/ai/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify({
                            context: "Какашка - это смесь выделенного уксуса и водорода",
                            question: messageText,
            
                        }),
                    });
                    const data = await response.json();
                    if(!response.ok){
                        console.error("Ошибка выполнения запроса: ",response, data)
                        addMessage(data.detail || 'Не удалось получить ответ от AI.', false);
                        return;
                    }
                    addMessage(data.answer,false);
                } catch (error){
                    console.error(error);
                }
    }

}

chatSendBtn.addEventListener('click', handleChatSend);
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
    startScreen.classList.remove('hidden');
    messagesArea.classList.add('hidden');
    chatInputArea.classList.remove('active');
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
    alert('Выход из аккаунта (демо)');
    profileDropdown.classList.remove('active');
});

fileInput.addEventListener('change', function (e) {
    selectedFile = e.target.files[0];

    if (!selectedFile) {
        return;
    }

    selectedFilePreview.classList.remove('hidden');
    selectedFilePreview.innerHTML = `
        <span>📄 ${selectedFile.name}</span>
        <button class="file-remove-btn" type="button" id="removeFileBtn">×</button>
    `;

    document.getElementById('removeFileBtn').addEventListener('click', function () {
        selectedFile = null;
        fileInput.value = '';
        selectedFilePreview.classList.add('hidden');
        selectedFilePreview.innerHTML = '';
    });
});

startInput.focus();
