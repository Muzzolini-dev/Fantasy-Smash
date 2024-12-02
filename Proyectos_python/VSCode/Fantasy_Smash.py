from functools import lru_cache
from numpy import ceil
from numpy.random import choice, randint
from enum import Enum

class Maestria(Enum):
    """Define con la clase Enum las dos posibles maestrías"""
    FISICO = "fisico"
    MAGICO = "magico"
    
class Constantes_combate:
    # Multiplicadores
    MULTIPLICADOR_PRECISION = 15
    MULTIPLICADOR_CRITICO = 2

    # Límites y umbrales
    MAX_PROBABILIDAD = 100
    LIMITE_DAMAGE_MINIMO = -2
    MIN_DAMAGE = 1
    NO_DAMAGE = 0
    LIMITE_CONTROL_VELOCIDAD = 2

    # Curaciones
    RATIO_CURACION_CLERIGO = 3
    CURACION_VICTORIA = 10
    MAX_VIDA_VICTORIA = 21
    
class Personaje:
    """Clase base para personajes. Define estadísticas y mecánicas de combate."""
    def __init__(self, nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria):
        self.__nombre = nombre
        self.__vida = vida
        self.__fuerza = fuerza
        self.__defensa = defensa
        self.__magia = magia
        self.__resistencia = resistencia
        self.__velocidad = velocidad
        self.__habilidad = habilidad
        self.__suerte = suerte
        self.__maestria = maestria
        
        
    def get_stats(self):
        print(f'''{self.__nombre}:
Vida: {self.__vida}
Fuerza: {self.__fuerza}
Defensa: {self.__defensa}
Magia: {self.__magia}
Resistencia: {self.__resistencia}
Velocidad: {self.__velocidad}
Habilidad: {self.__habilidad}
Suerte: {self.__suerte}
''')
        
    #Estas 4 funciones son para mejorar el metodo atacar y adaptarlo a la subclase Clérigo
    def get_nombre(self) -> str:
        return self.__nombre
        
    def get_vida(self) -> int:
        return self.__vida
    
    def set_vida(self, nueva_vida) -> int:
        if nueva_vida < 0:
            nueva_vida = 0
        self.__vida = nueva_vida
        
    def set_magia (self, nueva_magia) -> int:
        if nueva_magia < 0:
            nueva_magia = 0
        self.__magia = nueva_magia
        
    #Estos 3 getters me ayudan para hacer que el decorador @lru_cache cumpla su función al recibir los parametros exactos

        
    def daño_fisico(self, enemigo) -> int:
        if (ceil(self.__fuerza - enemigo.__defensa) <= 0):
            return Constantes_combate.MIN_DAMAGE 
        elif (ceil(self.__fuerza - enemigo.__defensa) <= Constantes_combate.LIMITE_DAMAGE_MINIMO): 
            return Constantes_combate.NO_DAMAGE 
        else:
            return int(ceil(self.__fuerza -enemigo.__defensa))
        
    def daño_magico(self, enemigo) -> int:
        if (ceil(self.__magia - enemigo.__resistencia) <= 0):
            return Constantes_combate.MIN_DAMAGE
        elif (ceil(self.__magia - enemigo.__resistencia) <= Constantes_combate.LIMITE_DAMAGE_MINIMO): 
            return Constantes_combate.NO_DAMAGE
        else:
            return int(ceil(self.__magia -enemigo.__resistencia))
        
    def control_velocidad(self, enemigo) -> bool:
        """Retorna True si el atacante supera en 2 o más la velocidad del defensor, para proceder a un ataque doble, False en caso contrario"""
        if (self.__velocidad - enemigo.__velocidad >= Constantes_combate.LIMITE_CONTROL_VELOCIDAD):
            return True
        return False
    
    def probabilidad_critico(self, enemigo) -> int:
        if(round((self.__habilidad + self.__suerte) - enemigo.__suerte) * Constantes_combate.MULTIPLICADOR_CRITICO >= Constantes_combate.MAX_PROBABILIDAD):
            return Constantes_combate.MAX_PROBABILIDAD
        else:
            return round((self.__habilidad + self.__suerte) - enemigo.__suerte) * Constantes_combate.MULTIPLICADOR_CRITICO
    
    def precision(self, enemigo) -> int:
        if (round((self.__habilidad + self.__velocidad) - (enemigo.__habilidad)) * Constantes_combate.MULTIPLICADOR_PRECISION >= Constantes_combate.MAX_PROBABILIDAD):
            return Constantes_combate.MAX_PROBABILIDAD
        else:
            return round((self.__habilidad + self.__velocidad) - (enemigo.__habilidad)) * Constantes_combate.MULTIPLICADOR_PRECISION
           
    def casos_atacar(self, enemigo) -> int:
        """Determina y ejecuta el tipo de ataque basado en la maestría y control.
        Args:
            enemigo (Personaje): Objetivo del ataque
        Returns:
            int: Daño total realizado
        Raises:
            ValueError: Si la maestría no es reconocida"""
        control = self.control_velocidad(enemigo)
        precision = self.precision(enemigo)
        critico = self.probabilidad_critico(enemigo)
        match (self.__maestria, control):
            case(Maestria.FISICO, True):
                return self._atacar(enemigo, self.daño_fisico, precision, critico, doble_ataque=True)
           
            case (Maestria.FISICO, False):
                return self._atacar(enemigo, self.daño_fisico, precision, critico, doble_ataque=False)
            
            case (Maestria.MAGICO, True):
                return self._atacar(enemigo, self.daño_magico, precision, critico, doble_ataque=True)
            
            case (Maestria.MAGICO, False):
                return self._atacar(enemigo, self.daño_magico, precision, critico, doble_ataque=False)
            
            case _:
                print("Acción no reconocida")
                return 0
            
    def _atacar(self, enemigo, funcion_daño, precision, critico, doble_ataque):
        """Ejecuta ataque base o doble según control de velocidad.
        Segundo golpe hace 80% del daño base.
        retorna el daño individual o doble"""
        daño_1 = self._daño_final(funcion_daño(enemigo), precision, critico)
        enemigo.__vida -= daño_1
        print(f"{self.__nombre} ha infligido {daño_1} puntos de daño a {enemigo.__nombre}")
    
        if doble_ataque:
            daño_2 = self._daño_final(round(funcion_daño(enemigo) * 0.8), precision, critico)
            enemigo.__vida -= daño_2
            print(f"{self.__nombre} ha infligido {daño_2} puntos de daño a {enemigo.__nombre}")
            return daño_1 + daño_2
        
        return daño_1
    
    def _daño_final(self, daño_base, precision, critico):
        """Calcula daño final considerando:
        - Acierto: daño_base o 0 según precision %
        - Crítico: daño_base*2 o daño_base según critico %
        Retorna 1 si hay error."""
        try:
            acierto = int(choice([daño_base, 0], p=[precision/100, (100-precision)/100]))
            critico_valor = int(choice([daño_base * 2, daño_base], p=[critico/100, (100-critico)/100]))
            return critico_valor if critico_valor else acierto
        except ValueError as e:
            print(f"Ha ocurrido un error {e} en el calculo de -daño_final()")
            return 1
                
        

class Mago (Personaje):
    """Clase Mago típica de rpg, pega duro y es fragil, 
    sus potenciadores son 2 o 3 a a magia, 1 o 2 a la resistencia y 1 a la defensa"""
    def __init__(self, nombre="Mago"):
        hechizo = randint(2, 4)
        tunica = randint(1,3)
        vida = 19
        fuerza = 2
        defensa = 3 + ceil(tunica/2)
        magia = 6 + hechizo
        resistencia = 3 + tunica
        velocidad = 6
        habilidad = 10
        suerte = 5
        maestria = Maestria.MAGICO
    
        super().__init__(nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria)
 
        
class Clerigo (Personaje):
    """Clase Clérigo típica de rpg, aguanta bien y se cura mientras pelea, 
    sus potenciadores son 1 o 2 a la magia, 2 o 3 a la resistencia y 1 o 2 a la defensa"""
    def __init__(self, nombre="Clérigo"):
        hechizo = randint(1, 3)
        tunica = randint(2,4)
        vida = 20
        fuerza = 2
        defensa = 3 + ceil(tunica/2)
        magia = 4 + hechizo
        resistencia = 5 + tunica
        velocidad = 4
        habilidad = 10
        suerte = 7
        maestria = Maestria.MAGICO
    
        super().__init__(nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria)
        
    def atacar(self, enemigo) -> int:
          # Llama al atacar original de la clase padre
        
        if isinstance(enemigo, Clerigo):  # Si hizo daño
            """Este if se hace para que un combate entre clerigos no dure una eternidad"""
            self.set_magia(9) 
            daño_realizado = super().casos_atacar(enemigo)
            return daño_realizado
            
        else:
            self.set_magia(4)
            daño_realizado = super().casos_atacar(enemigo)
            try:
                curacion = int(ceil(daño_realizado/ Constantes_combate.RATIO_CURACION_CLERIGO))
                self.set_vida(min(self.get_vida() + curacion, 20))
                print(f"{self.get_nombre()} se ha curado {curacion} y ahora tiene {self.get_vida()} puntos de vida")
                
            except Exception as e:
                print(f"Ha ocurrido un error {e} de forma inesperada mientras el clerigo se curaba. ")
                
            return daño_realizado
        
    
        
class Guerrero (Personaje):
    """Clase Guerrero típica de rpg, tanque que pega duro, 
    sus potenciadores son 2 o 3 a la fuerza, 1 o 2 a la defensa y 1 a la resistencia"""
    def __init__(self, nombre="Guerrero"):
        hacha = randint(2, 4)
        armadura = randint(1,3)
        vida = 21
        fuerza = 6 + hacha
        defensa = 3 + armadura
        magia = 1
        resistencia = 2 + ceil(armadura/2)
        velocidad = 5
        habilidad = 10
        suerte = 6
        maestria = Maestria.FISICO
    
        super().__init__(nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria)
        
        
class Soldado (Personaje):
    """Clase Soldado típica de rpg, tanque defensivo, equilibrado, 
    sus potenciadores son 1 o 2 a la fuerza, 2 o 3 a la defensa y 1 o 2 a la resistencia"""
    def __init__(self, nombre="Soldado"):
        lanza = randint(1, 3)
        armadura = randint(2,4)
        vida = 21
        fuerza = 5 + lanza
        defensa = 6 + armadura
        magia = 1
        resistencia = 3 + ceil(armadura/2)
        velocidad = 4
        habilidad = 10
        suerte = 5
        maestria = Maestria.FISICO
    
        super().__init__(nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria)
        
class Espadachin (Personaje):
    """Clase Espadachín típica de rpg, cañon de cristal que pega duro y con alto índice de critico, 
    sus potenciadores son 2 o 3 a la fuerza, 1 o 2 a la defensa y 1 a la habilidad"""
    def __init__(self, nombre="Espadachín"):
        espada = randint(2, 4)
        armadura = randint(1,3)
        vida = 19
        fuerza = 5 + espada
        defensa = 4 + armadura
        magia = 1
        resistencia = 3
        velocidad = 6
        habilidad = 11 + ceil(armadura/2)
        suerte = 5
        maestria = Maestria.FISICO
    
        super().__init__(nombre, vida, fuerza, defensa, magia, resistencia, velocidad, habilidad, suerte, maestria)
        
def turno():
    hero.atacar(enemy)
    if enemy.get_vida() <= 0:
        enemy.set_vida(0)  # Asegura que la vida no sea negativa
        print(f"{enemy.get_nombre()} ha muerto")
        hero.set_vida(min(hero.get_vida() + Constantes_combate.CURACION_VICTORIA, Constantes_combate.MAX_VIDA_VICTORIA))
        print(f"{hero.get_nombre()} se ha curado! (Y puede ser que esté más sano que nunca)")   
        return False
    print(f"{enemy.get_nombre()} tiene {enemy.get_vida()} puntos de vida")
    
    enemy.atacar(hero)
    if hero.get_vida() <= 0:
        hero.set_vida(0)  # Asegura que la vida no sea negativa
        print(f"{hero.get_nombre()} ha muerto")    
        return False
    print(f"{hero.get_nombre()} tiene {hero.get_vida()} puntos de vida")
    
hero = Clerigo("Hero")
enemy = Clerigo("Enemy")

for n in range(100):
    print(f"Turno {n+1}")
    turno()
    print("\n")
    if enemy.get_vida() == 0:
        print(f"{hero.get_nombre()} gana!!")
        break
    elif hero.get_vida() == 0:
        print(f"{enemy.get_nombre()} gana!!")
        break
    else:
        print("Estamos llegando correctamente al else \n")

