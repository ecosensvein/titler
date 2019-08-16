const app = new Vue({
    el: "#app",
    data: {
        log_area: "",
        urls_area: "",
        urls: [],
        status: "disconnected"
    },

    created: function() {
        this.connect();
    },

    methods: {
        connect() {
            this.socket = new WebSocket('ws://' + window.location.host);
            this.socket.onopen = () => {
                this.status = "connected";
                this.socket.onmessage = ({
                    data
                }) => {
                    var data = JSON.parse(data);
                    let newline = String.fromCharCode(13, 10);
                    let log_area = data['log_area'];
                    let urls_area = data['urls_area'];
                    let urls = data['urls'];
                    console.log(urls);
                    if (log_area) {
                        this.log_area = ""
                        for (const [key, value] of Object.entries(log_area)) {
                            this.log_area += (key + value + newline);
                        }
                    };
                    if (urls_area) {
                        this.urls_area = ""
                        for (const [key, value] of Object.entries(urls_area)) {
                            if (value) {
                                this.urls_area += (key + value + newline);
                            }
                        }
                    };
                    if (urls) {
                        this.urls = [];
                        for (const value of Object.entries(JSON.parse(urls))) {
                            this.urls.push({
                                id: value[1]["pk"],
                                url: value[1]["fields"]["url"],
                            })

                        }
                    };
                };
                this.socket.onclose = ({
                    data
                }) => {
                    this.status = "disconnected";
                    console.error('Socket closed unexpectedly');
                };
            };
        },
        sendMessage(e) {
            this.socket.send(JSON.stringify({
                id: e,
            }));
        }
    }
});
