const game = (function() {
    let state = {
      hero: null,
      enemy: null,
      turn: 0,
      battleNumber: 0,
      heroType: null,
      anonymous: true
    };
  
    function startNewGame(heroType) {
      console.log('startNewGame llamado con heroType:', heroType);
      state.heroType = heroType;
      state.battleNumber = 0;
      
      try {
        api.startNewGame(heroType, handleGameStart);
      } catch (error) {
        console.error('Error en startNewGame:', error);
        ui.showMessage('Error al iniciar el juego');
      }
    }
  
    function handleGameStart(data) {
        console.log('handleGameStart recibió data:', data);
        try {
            // Primero mostramos la pantalla de juego
            ui.showGameScreen();
            
            // Pequeña pausa para asegurar que el DOM está listo
            setTimeout(() => {
                try {
                    state.hero = data.hero;
                    state.enemy = data.enemy;
                    state.turn = 0;
                    
                    console.log('Actualizando stats con:', {
                        hero: state.hero,
                        enemy: state.enemy
                    });
                    
                    ui.updateCharacterStats(state.hero, state.enemy, data.hero_type);
                    ui.updateInitialSprites(data.hero_type, data.enemy.clase);
                    ui.updateBattleInfo(state.battleNumber, state.enemy.clase);
                    ui.showMessage('¡Comienza la batalla!');
                } catch (error) {
                    console.error('Error al procesar datos de juego:', error);
                    ui.showMessage('Error al iniciar la batalla');
                }
            }, 100);
            
        } catch (error) {
            console.error('Error en handleGameStart:', error);
            ui.showMessage('Error al iniciar la batalla');
        }
    }
  
    function attack() {
      console.log('Iniciando ataque...');
      try {
        api.attack(handleAttackResult);
      } catch (error) {
        console.error('Error en attack:', error);
        ui.showMessage('Error al realizar el ataque');
      }
    }
  
    async function handleAttackResult(data) {
      console.log('handleAttackResult recibió data:', data);
      try {
          const attackButton = document.querySelector('.attack-btn');
          attackButton.disabled = true;
          // Primero el ataque del héroe
          await ui.animateAttack(true, state.heroType, state.enemy.clase);
          console.log('Ataque del héroe completado');
          
          // Procesamos resultados del héroe
          state.hero = data.hero_stats || data.hero;
          state.enemy.vida = data.enemy_hp;
          ui.updateCharacterStats(state.hero, state.enemy);
          
          let mensajeAtaque = `Daño causado: ${data.damage_dealt}`;
          if (data.healing !== undefined && data.healing > 0) {
              mensajeAtaque += ` | Curación: ${data.healing}`;
          }
          ui.showMessage(mensajeAtaque);
  
          // Ahora el contraataque del enemigo si hubo daño recibido
          if (data.damage_received) {
              console.log('Iniciando contraataque del enemigo');
              // Esperamos un momento después del ataque del héroe
              await new Promise(resolve => setTimeout(resolve, 500));
              // Realizamos el contraataque
              await ui.animateAttack(false, state.heroType, state.enemy.clase);
              ui.showMessage(`Daño recibido: ${data.damage_received}`);
          }
  
          // Finalmente procesamos el estado del juego
          if (data.game_completed) {
              ui.showGameCompletedScreen();
          } else if (data.game_over) {
              ui.showGameOverScreen();
          } else if (data.next_battle) {
              ui.showVictoryScreen();
          }

          // Solo habilitamos el botón después de que todo haya terminado
        if (!data.game_completed && !data.game_over && !data.next_battle) {
          attackButton.disabled = false;
      }


      } catch (error) {
          console.error('Error en handleAttackResult:', error);
          ui.showMessage('Error al procesar resultado del ataque');
      }
  }
    function nextBattle() {
      console.log('Iniciando siguiente batalla...');
      try {
        ui.hideModal('victory-screen');
        api.nextBattle(handleNextBattleResult);
      } catch (error) {
        console.error('Error en nextBattle:', error);
        ui.showMessage('Error al iniciar siguiente batalla');
      }
    }
  
    function handleNextBattleResult(data) {
      console.log('handleNextBattleResult recibió data:', data);
      try {
        if (data.game_completed) {
          ui.showGameCompletedScreen();
        } else {
          state.hero = data.hero;
          state.enemy = data.enemy;
          state.battleNumber = data.battle_number;

          if (state.enemy && state.enemy.clase) {
            ui.updateInitialSprites(state.heroType, state.enemy.clase);
        } else {
            console.error('Error: Datos del enemigo incompletos', state.enemy);
        }

          ui.updateBattleInfo(state.battleNumber, state.enemy.clase);
          ui.showMessage(`¡Comienza la batalla ${state.battleNumber + 1} contra ${state.enemy.clase}!`);
          ui.updateCharacterStats(state.hero, state.enemy);
        }
        const attackButton = document.querySelector('.attack-btn');
            if (attackButton) {
                attackButton.disabled = false;
          } 
      } 
      catch (error) {
        console.error('Error en handleNextBattleResult:', error);
        ui.showMessage('Error al procesar siguiente batalla');
      }
    }
  
    function restartGame() {
      console.log('Reiniciando juego...');
      try {
        ui.hideAllModals();
        ui.showSetupScreen();
        characters.deselectCharacter();
        state = {
          hero: null,
          enemy: null,
          turn: 0,
          battleNumber: 0,
          heroType: null,
          anonymous: true
        };
      } catch (error) {
        console.error('Error en restartGame:', error);
        ui.showMessage('Error al reiniciar el juego');
      }
    }
  
    // API pública
    return {
      startNewGame,
      attack,
      nextBattle,
      restartGame
    };
})();