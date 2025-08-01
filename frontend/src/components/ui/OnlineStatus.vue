<template>
    <div class="floating-users-panel" :class="{ 'panel-collapsed': isCollapsed }" ref="panelRef"
        :style="{ top: panelTop + 'px' }">
        <div class="panel-content">
            <div class="panel-header" @mousedown="startHeaderDrag" @click="handleHeaderClick">
                <i class="pi pi-users"></i>
                <span>Usuarios ({{ onlineCount }})</span>
            </div>

            <div class="panel-body">
                <div v-if="loading" class="loading-indicator">
                    <ProgressSpinner style="width: 30px; height: 30px" />
                </div>
                <div v-else-if="onlineUsers.length === 0" class="empty-message">
                    <i class="pi pi-users mr-2"></i>
                    No hay usuarios conectados
                </div>
                <div v-else class="users-list">
                    <div v-for="user in onlineUsers" :key="user.id" class="user-item">
                        <Badge severity="success" class="mr-2"></Badge>
                        <div class="user-info">
                            <span class="username">{{ user.username }}</span>
                            <span class="fullname">{{ user.fullname }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <button class="panel-toggle-button" :class="{ 'is-collapsed': isCollapsed }" @mousedown="startDrag"
            @click="handleButtonClick">
            <i class="pi pi-users"></i>
            <span class="badge">{{ onlineCount }}</span>
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const onlineUsers = ref([]);
const loading = ref(true);
const onlineCount = ref(0);
const isCollapsed = ref(true);
const panelRef = ref(null);
const panelTop = ref(0);
const isDragging = ref(false);
const hasDragged = ref(false);
const dragStartY = ref(0);
const dragStartTop = ref(0);

let socket = null;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;
const reconnectDelay = 3000;
let heartbeatInterval = null;

const connectWebSocket = () => {
    loading.value = true;

    const token = localStorage.getItem('auth_token');
    if (!token) {
        console.error('No authentication token available');
        loading.value = false;
        return;
    }

    const isSecure = window.location.protocol === 'https:';
    const wsProtocol = isSecure ? 'wss://' : 'ws://';
    const host = process.env.VUE_APP_WS_HOST || window.location.hostname;
    const port = process.env.VUE_APP_WS_PORT || (isSecure ? 443 : 8000);
    const wsUrl = `${wsProtocol}${host}:${port}/ws/online-status/`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        reconnectAttempts = 0;

        // Enviar token como primer mensaje
        socket.send(JSON.stringify({
            type: 'authenticate',
            token: token
        }));

        // Configurar heartbeat
        heartbeatInterval = setInterval(() => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'heartbeat' }));
            }
        }, 30000);
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);

            if (data.type === 'online_users') {
                onlineUsers.value = data.users;
                onlineCount.value = data.users.length;
                loading.value = false;
            } else if (data.type === 'authentication_success') {
                console.log('Autenticación WebSocket exitosa');
            }
        } catch (e) {
            console.error('Error parsing WebSocket message:', e);
        }
    };

    socket.onclose = (event) => {
        console.log('WebSocket cerrado:', event.code, event.reason);
        if (heartbeatInterval) clearInterval(heartbeatInterval);

        if (!event.wasClean && reconnectAttempts < maxReconnectAttempts) {
            setTimeout(() => {
                reconnectAttempts++;
                console.log(`Reconectando (intento ${reconnectAttempts}/${maxReconnectAttempts})...`);
                connectWebSocket();
            }, reconnectDelay);
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (heartbeatInterval) clearInterval(heartbeatInterval);
    };
};

const togglePanel = () => {
    isCollapsed.value = !isCollapsed.value;
};

const handleHeaderClick = (e) => {
    if (hasDragged.value) {
        e.preventDefault();
        return;
    }
    togglePanel();
};

const handleButtonClick = (e) => {
    if (hasDragged.value) {
        e.preventDefault();
        hasDragged.value = false;
        return;
    }
    togglePanel();
};

const startDrag = (e) => {
    if (!isCollapsed.value) return;

    isDragging.value = true;
    hasDragged.value = false;
    dragStartY.value = e.clientY;
    dragStartTop.value = panelTop.value;

    panelRef.value.classList.add('dragging-active');

    document.addEventListener('mousemove', handleDrag, { passive: false });
    document.addEventListener('mouseup', stopDrag, { passive: true });
    document.body.style.userSelect = 'none';
    e.preventDefault();
};

const startHeaderDrag = (e) => {
    if (isCollapsed.value) return;

    isDragging.value = true;
    hasDragged.value = false;
    dragStartY.value = e.clientY;
    dragStartTop.value = panelTop.value;

    panelRef.value.classList.add('dragging-active');

    document.addEventListener('mousemove', handleDrag, { passive: false });
    document.addEventListener('mouseup', stopDrag, { passive: true });
    document.body.style.userSelect = 'none';
    e.preventDefault();
};

const handleDrag = (e) => {
    if (!isDragging.value) return;
    e.preventDefault();

    // Detect if we've dragged more than 5px to consider it a drag
    if (Math.abs(e.clientY - dragStartY.value) > 5) {
        hasDragged.value = true;
    }

    const deltaY = e.clientY - dragStartY.value;
    let newTop = dragStartTop.value + deltaY;

    requestAnimationFrame(() => {
        panelTop.value = Math.max(0, Math.min(window.innerHeight - 44, newTop));
    });
};

const stopDrag = () => {
    if (!isDragging.value) return;

    isDragging.value = false;
    panelRef.value.classList.remove('dragging-active');
    document.body.style.userSelect = '';

    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', stopDrag);

    // Small delay to allow click event to check hasDragged
    setTimeout(() => {
        hasDragged.value = false;
    }, 100);
};

onMounted(() => {
    panelTop.value = window.innerHeight / 2 - 22;
    connectWebSocket();

    window.addEventListener('resize', () => {
        panelTop.value = Math.min(panelTop.value, window.innerHeight - 44);
    });
});

onUnmounted(() => {
    if (socket) {
        socket.close();
    }
    if (heartbeatInterval) clearInterval(heartbeatInterval);
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', stopDrag);
});
</script>

<style scoped>
.floating-users-panel {
    position: fixed;
    right: 0;
    z-index: 100;
    /* Valor intermedio seguro */
    display: flex;
    contain: layout;
    backface-visibility: hidden;
    transform: translate3d(0, 0, 0);
    pointer-events: none;
    /* Permite clicks a través del panel */
}

.floating-users-panel.dragging-active {
    transition: none !important;
}

.panel-content {
    width: 200px;
    background: rgba(255, 255, 255, 0.98);
    border-radius: 12px 0 0 12px;
    box-shadow: -4px 0 15px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-right: none;
    overflow: hidden;
    /* Asegura que no haya overflow */
    backdrop-filter: blur(5px);
    transform-origin: right center;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
    will-change: transform, opacity;
}

.panel-header {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    cursor: pointer;
    font-weight: 600;
    color: #2d3748;
    transition: all 0.2s ease;
    user-select: none;
}

.panel-header:hover {
    background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
}

.panel-header i {
    margin-right: 0.5rem;
    color: #3B82F6;
}

.panel-body {
    max-height: 400px;
    overflow: hidden;
    /* Desactivamos completamente el scroll */
    padding: 0.75rem;
    display: flex;
    flex-direction: column;
}

/* Ocultar scrollbar en WebKit (Chrome, Safari) */
.panel-body::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
    background: transparent;
}

.users-list {
    flex: 1;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.user-item {
    display: flex;
    align-items: center;
    padding: 0.75rem;
    border-radius: 8px;
    transition: all 0.2s ease;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(0, 0, 0, 0.03);
    will-change: transform;
}

.user-item:hover {
    background: #f8fafc;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    transform: translateY(-1px);
}

.user-info {
    display: flex;
    flex-direction: column;
    margin-left: 0.75rem;
    flex-grow: 1;
}

.username {
    font-weight: 600;
    font-size: 0.9rem;
    color: #1a202c;
}

.fullname {
    font-size: 0.8rem;
    color: #718096;
}

.loading-indicator {
    display: flex;
    justify-content: center;
    padding: 1.5rem;
}

.empty-message {
    padding: 1.5rem;
    text-align: center;
    color: #a0aec0;
    font-style: italic;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
}

.empty-message i {
    margin-right: 0.5rem;
}

.panel-toggle-button {
    position: absolute;
    right: 0;
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    color: white;
    border: none;
    border-radius: 50% 0 0 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 10;
    clip-path: circle(71% at 50% 50%);
    will-change: transform;
    transform: translate3d(0, 0, 0);
    pointer-events: auto;
    /* El botón siempre debe ser clickeable */

}

.panel-toggle-button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    transform: scale(1.05) translate3d(0, 0, 0);
    box-shadow: -3px 0 7px rgba(0, 0, 0, 0.15);
}

.panel-toggle-button.is-collapsed {
    cursor: grab;
}

.panel-toggle-button.is-collapsed:active {
    cursor: grabbing;
}

.panel-toggle-button .badge {
    position: absolute;
    top: -6px;
    right: -6px;
    background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
    color: white;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.panel-collapsed .panel-content {
    transform: translateX(100%);
    /* Mueve completamente fuera de pantalla */
    opacity: 0;
    width: 0;
    border: none;
    padding: 0;
    margin: 0;
    pointer-events: none;
    /* Desactiva interacción cuando está colapsado */
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(5px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.user-item {
    animation: fadeIn 0.3s ease forwards;
}

.user-item:nth-child(1) {
    animation-delay: 0.05s;
}

.user-item:nth-child(2) {
    animation-delay: 0.1s;
}

.user-item:nth-child(3) {
    animation-delay: 0.15s;
}

.user-item:nth-child(4) {
    animation-delay: 0.2s;
}

.user-item:nth-child(5) {
    animation-delay: 0.25s;
}
</style>