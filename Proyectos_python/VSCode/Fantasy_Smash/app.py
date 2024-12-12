from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from game import Constantes_combate, Clerigo, Espadachin, Soldado, Guerrero, Mago
from db import Database

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'
db = Database()

# Estado del juego
game_state = {
    'hero': None,
    'enemy': None,
    'turn': 0,
    'battle_number': 0,
    'hero_type': None,
    'anonymous': True
}

def get_character_classes():
    return {
        'Clérigo': Clerigo,
        'Guerrero': Guerrero,
        'Mago': Mago,
        'Soldado': Soldado,
        'Espadachín': Espadachin
    }

def next_enemy_type() -> str:
    """Determina el siguiente tipo de enemigo basado en la batalla actual"""
    all_classes = ['Clérigo', 'Guerrero', 'Mago', 'Soldado', 'Espadachín']
    
    if game_state['hero_type'] in all_classes:
        all_classes.remove(game_state['hero_type'])
    
    if game_state['battle_number'] < 4:
        return all_classes[game_state['battle_number']]
    else:
        return game_state['hero_type']

@app.route('/')
def index():
    return render_template('index.html', is_logged_in='user_id' in session)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        print("Intento de registro recibido")
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Usuario intentando registrarse: {username}")
        
        if db.create_user(username, password):
            print("registro exitoso")
            flash('Registro exitoso!\nPuedes iniciar sesión.')
            return redirect(url_for('index'))
        else:
            print("error en el registro")
            flash('Este usuario ya existe.')
            return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print("Intento de login recibido")
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Usuario intentando logearse: {username}")
        
        user_id = db.check_user(username, password)
        if user_id:
            print("login exitoso")
            session['user_id'] = user_id
            session['username'] = username
            game_state['anonymous'] = False
            print(f"Estado anonymous actualizado a: {game_state['anonymous']}")
            flash(f'Bienvenido {username}.')
            return redirect(url_for('index'))
        else:
            print("login fallido")
            flash('Usuario o contraseña incorrectos.')
            return redirect(url_for('index'))
        
@app.route('/update_username', methods=['POST'])
def update_username():
    if request.method == 'POST':
        username = request.form.get('username')
        new_username = request.form.get('new_username')
        password = request.form.get('password')
        
        updated_username = db.update_user(username, new_username, password)
        if updated_username:
            session['username'] = new_username
            flash('Username actualizado exitosamente!')
            return redirect(url_for('index'))
        else:
            flash('Error al actualizar \nel username')
            return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if db.delete_user(username, password):
            session.clear()
            flash('Usuario eliminado \nexitosamente')
            return redirect(url_for('index'))
        else:
            flash('Error al eliminar \nel usuario')
            return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    game_state['anonymous'] = True
    flash('Sesión cerrada :d')
    return redirect(url_for('index'))

@app.route('/get_character_stats/<character_type>')
def get_character_stats(character_type):
    character_classes = get_character_classes()
    temp_character = character_classes[character_type]()
    return jsonify(temp_character.get_stats())

@app.route('/new_game', methods=['POST'])
def new_game():
    try:
        game_state['anonymous'] = 'user_id' not in session
        print(f"Iniciando juego - Estado anonymous: {game_state['anonymous']}")
        data = request.get_json()
        if not data or 'character_type' not in data:
            return jsonify({'error': 'No se proporcionó tipo de personaje'}), 400
            
        character_type = data['character_type']
        game_state['hero_type'] = character_type
        game_state['battle_number'] = 0
        
        character_classes = get_character_classes()
        
        # Agregar log para debugging
        print(f"Tipo de personaje recibido: {character_type}")
        print(f"Clases disponibles: {list(character_classes.keys())}")
        
        if character_type not in character_classes:
            return jsonify({'error': f'Tipo de personaje inválido: {character_type}'}), 400
        
        # Crear héroe y enemigo
        hero = character_classes[character_type]("Héroe")
        first_enemy_type = next_enemy_type()
        enemy = character_classes[first_enemy_type]("Enemigo")
        
        game_state['hero'] = hero
        game_state['enemy'] = enemy
        game_state['turn'] = 0
        
        response_data = {
            'hero': hero.get_stats(),
            'hero_type': character_type,
            'enemy': {
                'vida': enemy.get_vida(),
                'nombre': enemy.get_nombre(),
                'clase': first_enemy_type
            },
            'enemy_hp': enemy.get_vida(),
            'battle_number': game_state['battle_number']
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error en new_game: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/attack', methods=['POST'])
def attack():
    print(f"Estado de la sesión: {session}")  # Verificar estado de sesión
    print(f"Estado de anonymous: {game_state['anonymous']}")  # Verificar anonymous
    
    if not game_state['hero'] or not game_state['enemy']:
        return jsonify({'error': 'Juego no iniciado'}), 400
        
    hero = game_state['hero']
    enemy = game_state['enemy']
    
    try:
        # Manejar el caso especial del Clérigo
        if isinstance(hero, Clerigo):
            attack_result = hero.casos_atacar(enemy)
            result = {
                'damage_dealt': attack_result['damage'],
                'healing': attack_result['healing'],
                'hero_stats': hero.get_stats(),
                'enemy_hp': max(0, enemy.get_vida()),
                'message': []
            }
        else:
            # Comportamiento normal para otras clases
            damage_dealt = hero.casos_atacar(enemy)
            result = {
                'damage_dealt': damage_dealt,
                'hero_stats': hero.get_stats(),
                'enemy_hp': max(0, enemy.get_vida()),
                'message': []
            }
        
        enemy.set_vida(max(0, enemy.get_vida()))
        game_state['turn'] += 1
        
        # Verificar si el enemigo fue derrotado
        if enemy.get_vida() <= 0:
            print("Enemigo derrotado")  # Log de enemigo derrotado
            game_state['battle_number'] += 1
            print(f"Batalla número: {game_state['battle_number']}")  # Log número de batalla
            
            # Victoria total - completó todas las batallas
            if game_state['battle_number'] >= 5:
                print("Victoria total alcanzada")  # Log victoria total
                if not game_state['anonymous'] and 'user_id' in session:
                    print(f"Guardando victoria para usuario {session['user_id']}")
                    success = db.create_game(
                        session['user_id'],
                        game_state['hero_type'],
                        5,  
                        True  
                    )
                    print(f"Guardado {'exitoso' if success else 'fallido'}")  # Log resultado guardado
                else:
                    print("Usuario anónimo o sin sesión - Victoria no guardada")
                    
                result['game_completed'] = True
                result['message'].append("¡Has completado todas las batallas!")
                if game_state['anonymous']:
                    result['message'].append("¡Regístrate para aparecer en la clasificación!")
                return jsonify(result)
                
            hero.set_vida(min(hero.get_vida() + Constantes_combate.CURACION_VICTORIA, 
                             Constantes_combate.MAX_VIDA_VICTORIA))
            result['message'].append(f"¡Victoria! {hero.get_nombre()} se ha curado.")
            result['next_battle'] = True
            return jsonify(result)
        
        # Contraataque del enemigo
        if isinstance(enemy, Clerigo):
            enemy_attack = enemy.casos_atacar(hero)
            result['damage_received'] = enemy_attack['damage']
        else:
            result['damage_received'] = enemy.casos_atacar(hero)
        
        hero.set_vida(max(0, hero.get_vida()))
        result['hero_stats'] = hero.get_stats()  
        
        # Verificar si el héroe fue derrotado
        if hero.get_vida() <= 0:
            print("Héroe derrotado")  # Log héroe derrotado
            if not game_state['anonymous'] and 'user_id' in session:
                print(f"Guardando derrota para usuario {session['user_id']}")
                success = db.create_game(
                    session['user_id'],
                    game_state['hero_type'],
                    game_state['battle_number'],
                    False
                )
                print(f"Guardado {'exitoso' if success else 'fallido'}")  # Log resultado guardado
            else:
                print("Usuario anónimo o sin sesión - Derrota no guardada")
            
            result['game_over'] = True
            result['message'].append("¡Has sido derrotado!")
            if game_state['anonymous']:
                result['message'].append("¡Regístrate para aparecer en la clasificación!")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error en attack: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/next_battle', methods=['POST'])
def next_battle():
    if game_state['battle_number'] >= 5:
        return jsonify({
            'game_completed': True,
            'message': '¡Has completado todas las batallas!'
        })
    
    character_classes = get_character_classes()
    enemy_type = next_enemy_type()
    game_state['enemy'] = character_classes[enemy_type]("Enemigo")
    
    return jsonify({
        'hero': game_state['hero'].get_stats(),
        'enemy': {
            'vida': game_state['enemy'].get_vida(),
            'nombre': game_state['enemy'].get_nombre(),
            'clase': enemy_type
        },
        'battle_number': game_state['battle_number']
    })

@app.route('/login_after_game', methods=['POST'])
def login_after_game():
    """Endpoint para login después de completar una partida"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    user_id = db.check_user(username, password)
    if user_id:
        session['user_id'] = user_id
        session['username'] = username
        game_state['anonymous'] = False
        
        # Guardar la partida que acaba de completar
        if game_state.get('battle_number'):
            db.create_game(
                user_id,
                game_state['hero_type'],
                game_state['battle_number'],
                game_state['battle_number'] >= 5
            )
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'})

@app.route('/ranking')
def ranking():
    rankings = db.get_ranking()
    return render_template(
        'ranking.html', rankings=rankings,is_logged_in='user_id' in session)

if __name__ == '__main__':
    app.run(debug=True)