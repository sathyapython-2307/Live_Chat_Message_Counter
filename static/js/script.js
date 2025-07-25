function updateMessageCount() {
    fetch('/api/messages/count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('messageCount').textContent = data.count;
        });
}
updateMessageCount();
setInterval(updateMessageCount, 10000);