class Socket {
    constructor(url) {
        this.url = url;
        console.log(this.url);
        this.socket = null;
    }

    connect() {
        this.socket = io.connect(this.url);
        this.socket.on('connect', () => {
            console.log("Connected to server!");
        })

        this.socket.on('disconnect', () => {
            console.log("Disconnected from server!");
        })

        this.socket.on('error', (e) => {
            console.log(e);
        })

    }

    disconnect() {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    send(payload) {
        if (!this.socket) {
            this.connect();
        }
        let json = JSON.stringify(payload);
        this.socket.emit("message", json);
    }
    
    addMessageListener(channel, callback) {
        if (this.socket) {
            this.socket.on(channel, callback)
        }
    }

    removeMessageListener(channel, callback) {
        if (this.socket) {
            this.socket.off(channel, callback)
        }
    }
}