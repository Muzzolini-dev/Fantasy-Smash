
window.ir_a_ranking = function() {
  window.location.href = '/ranking';
}

window.showLoginModal = function() {
  ui.showLoginModal();
}

window.showRegisterModal = function() {
  ui.showRegisterModal();
}


window.showChangeUsernameModal = function() {
  document.getElementById('change-username-modal').style.display = 'flex';
}

window.showDeleteUserModal = function()  {
  document.getElementById('delete-user-modal').style.display = 'flex';
}

const ui = (function() {
    function showSetupScreen() {
      document.getElementById('setup-screen').style.display = 'block';
      document.getElementById('game-screen').style.display = 'none';
    }
  
    function showGameScreen() {
        try {
            const setupScreen = document.getElementById('setup-screen');
            const gameScreen = document.getElementById('game-screen');
            
            if (setupScreen && gameScreen) {
                setupScreen.style.display = 'none';
                gameScreen.style.display = 'block';
                
                console.log('Pantallas intercambiadas correctamente');
                
                // Verificar que los elementos necesarios existen
                const requiredElements = [
                    'hero-name',
                    'hero-hp',
                    'hero-health',
                    'enemy-name',
                    'enemy-hp',
                    'enemy-health',
                    'hero-stats'
                ];
                
                const missingElements = requiredElements.filter(id => !document.getElementById(id));
                if (missingElements.length > 0) {
                    console.error('Elementos faltantes:', missingElements);
                }
            } else {
                console.error('No se encontraron las pantallas necesarias');
            }
        } catch (error) {
            console.error('Error en showGameScreen:', error);
        }
    }
  
    function updateBattleInfo(battleNumber, enemyClass) {
      document.getElementById('battle-number').textContent = battleNumber + 1;
      document.getElementById('enemy-class').textContent = enemyClass;
    }
  
    function updateCharacterStats(hero, enemy, hero_type, updateTarget = 'both') {
        try {
            console.log('Actualizando stats con:', { hero, enemy });
            
            if (!hero || !enemy) {
                console.error('Datos de personajes incompletos:', { hero, enemy });
                return;
            }
    
            // Actualizar stats del héroe solo si se especifica 'hero' o 'both'
            if (updateTarget === 'hero' || updateTarget === 'both') {
                const heroName = document.getElementById('hero-name');
                const heroHp = document.getElementById('hero-hp');
                const heroHealth = document.getElementById('hero-health');
                
                if (heroName) heroName.textContent = hero.nombre;
                if (heroHp) heroHp.textContent = hero.vida;
                if (heroHealth) heroHealth.style.width = `${(hero.vida / 21) * 100}%`;
    
                // Actualizar el panel de stats siempre que se actualice la vida del héroe
                const heroStats = document.getElementById('hero-stats');
                if (heroStats) {
                    const statsHtml = `
                        <h3>Stats del ${hero_type || hero.nombre}</h3>
                        <div class="stat-grid">
                            <div>Vida:</div><div>${hero.vida}</div>
                            <div>Fuerza:</div><div>${hero.fuerza}</div>
                            <div>Defensa:</div><div>${hero.defensa}</div>
                            <div>Magia:</div><div>${hero.magia}</div>
                            <div>Resistencia:</div><div>${hero.resistencia}</div>
                            <div>Velocidad:</div><div>${hero.velocidad}</div>
                            <div>Habilidad:</div><div>${hero.habilidad}</div>
                            <div>Suerte:</div><div>${hero.suerte}</div>
                        </div>
                    `;
                    heroStats.innerHTML = statsHtml;
                }
            }
            
            // Actualizar stats del enemigo solo si se especifica 'enemy' o 'both'
            if (updateTarget === 'enemy' || updateTarget === 'both') {
                const enemyName = document.getElementById('enemy-name');
                const enemyHp = document.getElementById('enemy-hp');
                const enemyHealth = document.getElementById('enemy-health');
                
                if (enemyName) enemyName.textContent = enemy.nombre;
                if (enemyHp) enemyHp.textContent = enemy.vida;
                if (enemyHealth) enemyHealth.style.width = `${(enemy.vida / 21) * 100}%`;
            }
    
        } catch (error) {
            console.error('Error al actualizar stats:', error);
            ui.showMessage('Error al actualizar estadísticas');
        }
    }
  
    function showMessage(message) {
      const log = document.getElementById('combat-log');
      log.innerHTML += `<p>${message}</p>`;
      if (log.children.length > 4) {
        log.firstChild.remove();
      }
      log.scrollTop = log.scrollHeight;
    }
  
    function showModal(modalId) {
      document.getElementById(modalId).style.display = 'flex';
    }
  
    function hideModal(modalId) {
      document.getElementById(modalId).style.display = 'none';
    }
  
    function hideAllModals() {
      hideModal('victory-screen');
      hideModal('game-over-screen');
      hideModal('game-complete-screen');
    }
  
    function showVictoryScreen() {
      showModal('victory-screen');
    }
  
    function showGameOverScreen() {
      showModal('game-over-screen');
    }
  
    function showGameCompletedScreen() {
      showModal('game-complete-screen');
    }

    function showLoginModal() {
        closeModal('register-modal');
        document.getElementById('login-modal').style.display = 'flex';
      }
      
      function showRegisterModal() {
        closeModal('login-modal');
        document.getElementById('register-modal').style.display = 'flex';
      }
      
      function closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
      }
  
      function getSpriteUrls(characterClass) {
        const baseClass = characterClass.toLowerCase().replace('é', 'e').replace('í', 'i');
        let folder = '';
        
        switch(baseClass) {
            case 'clerigo':
                folder = 'cleric';
                break;
            case 'espadachin':
                folder = 'swordmaster';
                break;
            case 'guerrero':
                folder = 'warrior';
                break;
            case 'mago':
                folder = 'wizard';
                break;
            case 'soldado':
                folder = 'soldier';
                break;
        }
        
        return {
            stand: `static/images/${folder}/${folder}_stand.png`,
            attack: `static/images/${folder}/${folder}_attack.png`,
            damage: `static/images/${folder}/${folder}_damage.png`
        };
    }
    
    // Función para actualizar los sprites iniciales
    function updateInitialSprites(heroClass, enemyClass) {
        const heroSprites = getSpriteUrls(heroClass);
        const enemySprites = getSpriteUrls(enemyClass);
        
        const heroElement = document.querySelector('.hero img');
        const enemyElement = document.querySelector('.enemy img');
        
        if (!heroElement) {
            const heroImg = document.createElement('img');
            heroImg.src = heroSprites.stand;
            heroImg.alt = "Hero sprite";
            document.querySelector('.hero').appendChild(heroImg);
        } else {
            heroElement.src = heroSprites.stand;
        }
        
        if (!enemyElement) {
            const enemyImg = document.createElement('img');
            enemyImg.src = enemySprites.stand;
            enemyImg.alt = "Enemy sprite";
            document.querySelector('.enemy').appendChild(enemyImg);
        } else {
            enemyElement.src = enemySprites.stand;
        }
    }
    
    // Variable para controlar el estado de la animación
    let isAnimating = false;
    
    // Función para animar el ataque
    async function animateAttack(isHeroAttacking = true, heroType, enemyType) {
      console.log('Iniciando animación de ataque:', isHeroAttacking ? 'héroe' : 'enemigo');
      if (isAnimating) return;
      isAnimating = true;
      
      const heroElement = document.querySelector('.hero .character-sprite');
      const enemyElement = document.querySelector('.enemy .character-sprite');
      
      if (!heroElement || !enemyElement) {
          console.error('No se encontraron los elementos de sprite');
          isAnimating = false;
          return;
      }
      
      const heroSprites = getSpriteUrls(heroType);
      const enemySprites = getSpriteUrls(enemyType);
      
      const isMeleeClass = (type) => {
          return ['Espadachín', 'Soldado', 'Guerrero'].includes(type);
      };
      
      return new Promise((resolve) => {
          try {
              if (isHeroAttacking) {
                  // Héroe ataca
                  setTimeout(() => {
                      heroElement.src = heroSprites.attack;
                      // Solo agregar clases de animación si es físico
                      if (isMeleeClass(heroType)) {
                          heroElement.classList.add('attacking');
                          heroElement.classList.add('melee');
                      }
                  }, 200);
                  
                  setTimeout(() => {
                      enemyElement.src = enemySprites.damage;
                  }, 700);
                  
                  setTimeout(() => {
                      heroElement.src = heroSprites.stand;
                      if (isMeleeClass(heroType)) {
                          heroElement.classList.remove('attacking');
                          heroElement.classList.remove('melee');
                      }
                      enemyElement.src = enemySprites.stand;
                      isAnimating = false;
                      resolve();
                  }, 1000);
              } else {
                  // Enemigo ataca
                  setTimeout(() => {
                      enemyElement.src = enemySprites.attack;
                      // Solo agregar clases de animación si es físico
                      if (isMeleeClass(enemyType)) {
                          enemyElement.classList.add('attacking');
                          enemyElement.classList.add('melee');
                      }
                  }, 200);
                  
                  setTimeout(() => {
                      heroElement.src = heroSprites.damage;
                  }, 700);
                  
                  setTimeout(() => {
                      heroElement.src = heroSprites.stand;
                      enemyElement.src = enemySprites.stand;
                      if (isMeleeClass(enemyType)) {
                          enemyElement.classList.remove('attacking');
                          enemyElement.classList.remove('melee');
                      }
                      isAnimating = false;
                      resolve();
                  }, 1000);
              }
          } catch (error) {
              console.error('Error en animateAttack:', error);
              isAnimating = false;
              resolve();
          }
      });
  }

    return {
        showLoginModal,
        showRegisterModal,
        showChangeUsernameModal,
        showDeleteUserModal,
        closeModal,
        showSetupScreen,
        showGameScreen,
        updateBattleInfo,
        updateCharacterStats,
        showMessage,
        showModal,
        hideModal,
        hideAllModals,
        showVictoryScreen,
        showGameOverScreen,
        showGameCompletedScreen, 
        getSpriteUrls,
        updateInitialSprites,
        animateAttack
    };
  })();