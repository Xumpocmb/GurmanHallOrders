function hideNotification() {
        let notification = document.getElementById('notification');
        if (notification) {
            notification.style.display = 'none'; // Скрыть элемент
        }
    }

// Запустить функцию скрытия через 3 секунды
setTimeout(hideNotification, 3000); // 3000 миллисекунд = 3 секунды