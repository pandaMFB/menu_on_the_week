// Автоматическое скрытие сообщений через 5 секунд
setTimeout(function() {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        let closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
            closeButton.click();
        } else {
            alert.style.display = 'none';
        }
    });
}, 5000);

// Убираем подсветку с полей при фокусе (делегирование)
document.addEventListener('focusin', function(event) {
    const field = event.target;
    if (field.classList && field.classList.contains('is-invalid')) {
        field.classList.remove('is-invalid');
    }
});