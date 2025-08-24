// WebSocketTablero.js - SIN AUTENTICACIÓN
class WebSocketTablero {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 8;
    this.reconnectInterval = 2000;
    this.messageHandlers = new Map();
  }

  connect() {
    // Usar la variable de entorno para tableros o fallback
    const wsUrl = import.meta.env.VITE_API_URL_WS_TABLEROS || 
                 `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/tableros/`;
    
    console.log('Intentando conectar WebSocket a:', wsUrl);
    
    this.socket = new WebSocket(wsUrl);
    
    this.socket.onopen = () => {
      console.log('WebSocket conectado exitosamente');
      this.connected = true;
      this.reconnectAttempts = 0;
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket cerrado:', event.code, event.reason);
      this.connected = false;
      
      if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++;
          console.log(`Reconectando (intento ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
          this.connect();
        }, this.reconnectInterval);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.connected = false;
    };
  }

  handleReconnection() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Intentando reconectar (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        this.connect();
      }, this.reconnectInterval);
    }
  }

  handleMessage(data) {
    // Ejecutar todos los handlers registrados para este tipo de mensaje
    if (this.messageHandlers.has(data.type)) {
      const handlers = this.messageHandlers.get(data.type);
      handlers.forEach(handler => handler(data));
    }
  }

  on(messageType, handler) {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, []);
    }
    this.messageHandlers.get(messageType).push(handler);
  }

  off(messageType, handler) {
    if (this.messageHandlers.has(messageType)) {
      const handlers = this.messageHandlers.get(messageType);
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
      }
    }
  }

  send(message) {
    if (this.connected) {
      this.socket.send(JSON.stringify(message));
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.connected = false;
  }
}

// Crear una instancia única
export const webSocketTableroInstance = new WebSocketTablero();