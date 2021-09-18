const output = document.getElementById('console');
const socket = io();

socket.on("log-set", (log) => {
    output.innerText = log;
});