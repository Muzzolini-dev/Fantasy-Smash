document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM Cargado - Iniciando aplicación');
  
  // Inicializar carrusel de personajes
  try {
      console.log('Creando carrusel de personajes...');
      characters.createCharacterCards();
  } catch (error) {
      console.error('Error al crear carrusel:', error);
  }

  // Evento para botón de inicio
  document.querySelector('.start-button').addEventListener('click', function() {
    const selectedCharacter = characters.getSelectedCharacter();
    console.log('Personaje seleccionado:', selectedCharacter);
    
    if (selectedCharacter) {
      console.log('Iniciando nuevo juego con:', selectedCharacter);
      game.startNewGame(selectedCharacter);
    } else {
      console.log('No hay personaje seleccionado');
      ui.showMessage('Por favor selecciona un personaje');
    }
  });

  // Evento para botón de ataque
  document.querySelector('.attack-btn').addEventListener('click', function() {
      console.log('Botón de ataque presionado');
      game.attack();
  });

  // Evento para botón de siguiente batalla
  document.querySelector('.next-battle-button').addEventListener('click', function() {
    console.log('Iniciando siguiente batalla');
    game.nextBattle();
  });

  // Eventos para botones de reinicio
  document.querySelectorAll('.restart-button').forEach(button => {
    button.addEventListener('click', function() {
      console.log('Reiniciando juego');
      game.restartGame();
    });
  });

  console.log('Todos los event listeners configurados');

  // Código para cerrar modales (corregido)
  const loginModal = document.getElementById('login-modal');
  const registerModal = document.getElementById('register-modal');
  const closeButtons = document.querySelectorAll('.close');

  if (loginModal && registerModal && closeButtons) {
      closeButtons.forEach(button => {
          button.addEventListener('click', function() {
              const modal = this.closest('.modal-overlay');
              if (modal) {
                  modal.style.display = 'none';
              }
          });
      });

      window.addEventListener('click', function(event) {
          if (event.target.classList.contains('modal-overlay')) {
              event.target.style.display = 'none';
          }
      });
  }
});