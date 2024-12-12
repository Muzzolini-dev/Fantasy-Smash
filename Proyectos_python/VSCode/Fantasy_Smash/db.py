import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Optional, List, Dict

class Database:
    def __init__(self, nombre_db="game.db"):
        self.nombre_db = nombre_db
        self.init_db()
        
    def get_db(self) -> sqlite3.Connection:
        return sqlite3.connect(self.nombre_db) 
    
    def init_db(self) -> None:
        print("Conectando con db")
        conn = self.get_db()
        cursor = conn.cursor()
        
        #tabla de usuarios
        print("creando tablas en db si no existen")
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL, 
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER, character_class TEXT NOT NULL, 
                       battles_won INTEGER DEFAULT 0, completed_games INTEGER DEFAULT 0,
                       FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL)''')
        
        
        print("Verificando si las tablas se crearon...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tablas en la base de datos:", tables)
        conn.commit()
        conn.close()
        
    def create_user(self, username: str, password: str) -> bool:
        try:
            conn = self.get_db()
            cursor = conn.cursor()
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                     (username, password_hash))
            conn.commit()
            return True
        
        except sqlite3.IntegrityError:
            return False
        
        except Exception as e:
                print(f"Error no esperado {e}")
                return False
            
        finally:
            conn.close()
            
    def check_user(self, username: str, password: str) -> Optional[int]:
        '''Verificamos si el usuario y contraseña es correcto y retornamos su id en caso afirmativo'''
        conn = self.get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            return user[0]
        return None
    
    def update_user(self, username: str, new_username: str, password: str) -> str:
        '''Verificamos contraseña y usuario para modificar el nombre de usuario'''
        id = self.check_user(username, password)
        if id != None:
            try:
                conn = self.get_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, id,))
                cursor.execute("SELECT username FROM users WHERE id = ?", (id,))
                username_updated = cursor.fetchone()      
                conn.commit()          
                return username_updated
            
            except sqlite3.IntegrityError:
                return None
            
            except Exception as e:
                print(f"Error no esperado {e}")
                return None
            
            finally:
                conn.close()
        
    def delete_user(self, username: str, password: str) -> bool:
        '''Verificamos contraseña y usuario para eliminar al usuario'''
        id = self.check_user(username, password)
        if id:
            conn = self.get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        else:
            return False
        
    
    def create_game(self, user_id: int, character_class: str, battles_won: int, completed_games: bool) -> bool:
        '''Crea un registro de partida cuando termina el juego'''
        try:
            conn = self.get_db()
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO games (user_id, character_class, battles_won, completed_games)
            VALUES (?, ?, ?, ?)
            ''', (user_id, character_class, battles_won, 1 if completed_games else 0))
            
            conn.commit()
            print(f"Intentando guardar juego: user_id={user_id}, class={character_class}, wins={battles_won}, completed={completed_games}")
            return True
        
        except sqlite3.Error as e:
            print(f"Error al crear registro de partida: {e}")
            return False
        except Exception as e:
            print(f"Fallo inesperado {e}")
        finally:
            conn.close()
                
    def get_ranking(self) -> List[Dict]:
        """Obtiene la tabla de clasificación"""
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
            u.username,
            g.character_class,
            COUNT(CASE WHEN g.completed_games = 1 THEN 1 END) as completed_games,
            SUM(g.battles_won) as battles_won
        FROM users u
        LEFT JOIN games g ON u.id = g.user_id
        GROUP BY u.id, u.username
        ORDER BY battles_won DESC
        LIMIT 5
        ''')
        
        ranking = [{
            'username': row[0],
            'character_class': row[1],
            'completed_games': row[2],
            'battles_won': row[3] or 0
        } for row in cursor.fetchall()]
        
        conn.close()
        return ranking
            
        