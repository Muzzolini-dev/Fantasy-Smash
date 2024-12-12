const api = (function() {
    async function getCharacterStats(characterType, callback) {
      try {
        const response = await fetch(`/get_character_stats/${characterType}`);
        if (!response.ok) {
          throw new Error('Error al obtener stats');
        }
        const stats = await response.json();
        callback(stats);
      } catch (error) {
        console.error('Error:', error);
        ui.showMessage('Error al cargar stats');
      }
    }
  
    async function startNewGame(characterType, callback) {
      try {
        const response = await fetch('/new_game', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ character_type: characterType })
        });
  
        if (!response.ok) {
          throw new Error(`Error al iniciar el juego: ${response.status}`);
        }
  
        const data = await response.json();
        callback(data);
      } catch (error) {
        console.error('Error:', error);
        ui.showMessage('Error al iniciar el juego');
      }
    }
  
    async function attack(callback) {
      try {
        const response = await fetch('/attack', {
          method: 'POST'
        });
  
        if (!response.ok) {
          throw new Error(`Error en el ataque: ${response.status}`);
        }
  
        const data = await response.json();
        callback(data);
      } catch (error) {
        console.error('Error:', error);
        ui.showMessage('Error en el ataque');
      }
    }
  
    async function nextBattle(callback) {
      try {
        const response = await fetch('/next_battle', {
          method: 'POST'
        });
  
        if (!response.ok) {
          throw new Error('Error al cargar siguiente batalla');
        }
  
        const data = await response.json();
        callback(data);
      } catch (error) {
        console.error('Error:', error);
        ui.showMessage('Error al cargar siguiente batalla');
      }
    }
  
    return {
      getCharacterStats,
      startNewGame,
      attack,
      nextBattle
    };
  })();