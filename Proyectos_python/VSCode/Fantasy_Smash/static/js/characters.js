/* Lo que hace cada parte:

1. characterData: Objeto con todos los datos de los personajes
2. createCharacterCards(): Crea las tarjetas e inicializa el carrusel
3. setupNavigation(): Configura los botones de navegación
4. showCard(): Maneja la visualización de tarjetas en el carrusel
5. selectCharacter(): Maneja la selección de personajes
6. updateCharacterPreview(): Actualiza la vista previa de estadísticas
7. deselectCharacter(): Maneja la deselección
8. getSelectedCharacter(): Obtiene el personaje seleccionado actual */

const characters = (function() {
    // Datos estáticos de los personajes con sus sprites y estadísticas
    const characterData = {
      'Espadachín': {
        sprite: 'static/images/swordmaster/swordmaster_stand.png',
        stats: {
          Vida: '19',
          Fuerza: '5↑↑↑',
          Defensa: '4↑↑',
          Magia: '1',
          Resistencia: '3',
          Velocidad: '6',
          Habilidad: '11↑',
          Suerte: '5'
        }
      },
      
      'Mago': {
        sprite: 'static/images/wizard/wizard_stand.png',
        stats: {
          Vida: '19',
          Fuerza: '2',
          Defensa: '3↑',
          Magia: '6↑↑↑',
          Resistencia: '3↑↑',
          Velocidad: '6',
          Habilidad: '10',
          Suerte: '5'
        }
      },

      'Guerrero': {
        sprite: 'static/images/warrior/warrior_stand.png',
        stats: {
          Vida: '21',
          Fuerza: '6↑↑↑',
          Defensa: '3↑↑',
          Magia: '1',
          Resistencia: '2↑',
          Velocidad: '5',
          Habilidad: '10',
          Suerte: '6'
        }
      },

      'Clérigo': {
        sprite: 'static/images/cleric/cleric_stand.png',
        stats: {
          Vida: '20',
          Fuerza: '2',
          Defensa: '3↑',
          Magia: '4↑↑',
          Resistencia: '5↑↑↑',
          Velocidad: '4',
          Habilidad: '10',
          Suerte: '7'
        }
      },
      
      'Soldado': {
        sprite: 'static/images/soldier/soldier_stand.png',
        stats: {
          Vida: '21',
          Fuerza: '5↑↑',
          Defensa: '6↑↑↑',
          Magia: '1',
          Resistencia: '3↑',
          Velocidad: '4',
          Habilidad: '10',
          Suerte: '5'
        }
      }
    };
  
    // Variables de estado
    let selectedCharacter = null;
    let currentCard = 0;
  
    function createCharacterCards() {
      const container = document.querySelector('.card-container');
      const indicatorsContainer = document.querySelector('.carousel-indicators');
      
      // Limpiar contenedores
      container.innerHTML = '';
      indicatorsContainer.innerHTML = '';
  
      // Crear tarjetas de personajes e indicadores
      Object.entries(characterData).forEach(([displayName, data], index) => {
        // Crear tarjeta de personaje
        const card = document.createElement('div');
        card.className = 'character-card';
        card.dataset.character = displayName;
        
        // Crear contenido de la tarjeta
        const statsHtml = Object.entries(data.stats)
          .map(([stat, value]) => `<div>${stat}:</div><div>${value}</div>`)
          .join('');
        
        card.innerHTML = `
          <h3>${displayName}</h3>
          <img src="${data.sprite}" alt="${displayName}" class="character-sprite">
          <div class="character-stats">
            ${statsHtml}
          </div>
        `;
        
        // Agregar evento de selección
        card.addEventListener('click', () => selectCharacter(displayName));
        container.appendChild(card);
        
        // Crear indicador del carrusel
        const indicator = document.createElement('div');
        indicator.className = 'indicator' + (index === currentCard ? ' active' : '');
        indicator.addEventListener('click', () => showCard(index));
        indicatorsContainer.appendChild(indicator);
      });
      
      // Configurar navegación
      setupNavigation();
      
      // Mostrar primera tarjeta
      showCard(0);
    }

    function setupNavigation() {
      // Configurar botones de navegación
      const prevButton = document.createElement('button');
      prevButton.className = 'carousel-button prev';
      prevButton.textContent = '←';
      prevButton.onclick = () => showCard(currentCard - 1);

      const nextButton = document.createElement('button');
      nextButton.className = 'carousel-button next';
      nextButton.textContent = '→';
      nextButton.onclick = () => showCard(currentCard + 1);

      // Agregar botones al DOM
      const carousel = document.querySelector('.character-carousel');
      carousel.insertBefore(prevButton, carousel.firstChild);
      carousel.appendChild(nextButton);
    }
  
    function showCard(index) {
      const cards = document.querySelectorAll('.character-card');
      const indicators = document.querySelectorAll('.indicator');
      const totalCards = cards.length;
      
      // Asegurar que el índice esté dentro de los límites
      if (index < 0) index = totalCards - 1;
      if (index >= totalCards) index = 0;
      
      currentCard = index;
      
      // Actualizar posición de las tarjetas
      const offset = -index * (cards[0].offsetWidth + 40); // 40 es el gap entre tarjetas
      document.querySelector('.card-container').style.transform = `translateX(${offset}px)`;
      
      // Actualizar indicadores
      indicators.forEach((indicator, i) => {
        indicator.classList.toggle('active', i === index);
      });
    }
  
    function selectCharacter(characterType) {
      selectedCharacter = characterType;
      
      // Actualizar visualización de selección
      document.querySelectorAll('.character-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.character === characterType);
      });
      
      // Obtener y mostrar stats actualizados
      api.getCharacterStats(characterType, updateCharacterPreview);
    }
  
    function updateCharacterPreview(stats) {
      const previewElement = document.getElementById('character-preview');
      
      if (!selectedCharacter || !previewElement) return;
      
      previewElement.innerHTML = `
        <h3>Stats del ${selectedCharacter}</h3>
        <div class="stat-grid">
          <div>Vida:</div><div>${stats.vida}</div>
          <div>Fuerza:</div><div>${stats.fuerza}</div>
          <div>Defensa:</div><div>${stats.defensa}</div>
          <div>Magia:</div><div>${stats.magia}</div>
          <div>Resistencia:</div><div>${stats.resistencia}</div>
          <div>Velocidad:</div><div>${stats.velocidad}</div>
          <div>Habilidad:</div><div>${stats.habilidad}</div>
          <div>Suerte:</div><div>${stats.suerte}</div>
        </div>
      `;
    }
  
    function deselectCharacter() {
      selectedCharacter = null;
      
      // Limpiar selección visual
      document.querySelectorAll('.character-card').forEach(card => {
        card.classList.remove('selected');
      });
      
      // Restaurar preview por defecto
      const previewElement = document.getElementById('character-preview');
      if (previewElement) {
        previewElement.innerHTML = 'Aquí podrás ver las estadísticas de tu personaje';
      }
    }
  
    function getSelectedCharacter() {
      return selectedCharacter;
    }
  
    // API pública del módulo
    return {
      createCharacterCards,
      selectCharacter,
      deselectCharacter,
      getSelectedCharacter
    };
})();