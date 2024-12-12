// Objeto UI para los modales
window.ui = {
    showLoginModal: function() {
        document.getElementById('login-modal').style.display = 'flex';
    },
    showRegisterModal: function() {
        document.getElementById('register-modal').style.display = 'flex';
    }
};

// Función para volver al índice
window.volver_al_index = function() {
    window.location.href = '/';
}

document.addEventListener('DOMContentLoaded', function() {
    // Cerrar modales cuando se hace clic en la X
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal-overlay');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Cerrar modales cuando se hace clic fuera
    window.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal-overlay')) {
            event.target.style.display = 'none';
        }
    });
});