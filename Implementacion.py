import random

# 1. Función de evaluación del fitness (Minimizar costos)
def evaluar(individuo):
    """
    Evaluación del costo total para cada individuo.
    Cada individuo es una estrategia de operación con costos asociados a combustible, mantenimiento y operación.
    """
    costo_combustible = sum([x * 0.5 for x in individuo])  # Suponiendo que cada unidad de operación consume 0.5 unidades de combustible
    costo_mantenimiento = sum([x * 0.2 for x in individuo])  # Suponiendo que cada unidad de operación requiere un costo de mantenimiento de 0.2
    costo_operacion = sum([x * 50 for x in individuo])  # Ajuste de costo de operación, cada unidad que está en operación genera un costo adicional de 50
    
    return costo_combustible + costo_mantenimiento + costo_operacion

# 2. Inicialización de la población
def crear_individuo(tamano):
    """Crear un individuo con decisiones aleatorias (0 o 1) representando el uso de unidades."""
    return [random.randint(0, 1) for _ in range(tamano)]

def crear_poblacion(tamano_poblacion, tamano_individuo):
    """Crear una población inicial de individuos aleatorios."""
    return [crear_individuo(tamano_individuo) for _ in range(tamano_poblacion)]

# 3. Selección: método de torneo
def seleccion(poblacion):
    """Seleccionar un individuo de la población usando selección por torneo."""
    torneo_size = 5  # Puedes aumentar el tamaño del torneo para mayor diversidad
    torneo = random.sample(poblacion, torneo_size)
    torneo.sort(key=lambda x: x[1])  # Ordenar por fitness (en este caso, costos más bajos son mejores)
    return torneo[0][0]  # Devolver el mejor individuo (sin el costo)

# 4. Función de cruce (crossover)
def cruce(padre1, padre2):
    """Cruce de dos individuos (padres) para generar descendientes."""
    punto_cruce = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

# 5. Función de mutación
def mutacion(individuo, tasa_mutacion=0.2):
    """Aplicar una pequeña mutación al individuo para introducir variabilidad."""
    if random.random() < tasa_mutacion:
        idx = random.randint(0, len(individuo) - 1)
        individuo[idx] = 1 - individuo[idx]  # Invertir un bit (decisión de operación)
    return individuo

# 6. Algoritmo evolutivo principal
def algoritmo_evolutivo(tamano_poblacion, tamano_individuo, generaciones):
    poblacion = crear_poblacion(tamano_poblacion, tamano_individuo)
    
    # Evaluar la población inicial
    poblacion = [(individuo, evaluar(individuo)) for individuo in poblacion]
    
    mejor_individuo = min(poblacion, key=lambda x: x[1])  # El mejor individuo inicial (menor costo)
    print("Generación 0: Mejor costo =", mejor_individuo[1])
    
    for generacion in range(1, generaciones + 1):
        nueva_poblacion = []
        
        # Crear nuevos individuos mediante cruce y mutación
        while len(nueva_poblacion) < tamano_poblacion:
            padre1 = seleccion(poblacion)
            padre2 = seleccion(poblacion)
            hijo1, hijo2 = cruce(padre1, padre2)
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)
            
            nueva_poblacion.append((hijo1, evaluar(hijo1)))
            nueva_poblacion.append((hijo2, evaluar(hijo2)))
        
        # Seleccionar los mejores individuos para la siguiente generación
        poblacion = sorted(nueva_poblacion, key=lambda x: x[1])[:tamano_poblacion]
        
        # Evaluar el mejor individuo de la generación actual
        mejor_individuo_generacion = min(poblacion, key=lambda x: x[1])
        print(f"Generación {generacion}: Mejor costo = {mejor_individuo_generacion[1]}")
        
        # Si el mejor individuo tiene un costo mínimo, terminar
        if mejor_individuo_generacion[1] == 0:
            print("¡Se encontró la solución óptima!")
            break

    return mejor_individuo

# Parámetros
tamano_poblacion = 20  # Tamaño de la población
tamano_individuo = 10  # Número de decisiones (por ejemplo, unidades de operación)
generaciones = 100  # Número máximo de generaciones

# Ejecutar el algoritmo evolutivo
mejor_individuo = algoritmo_evolutivo(tamano_poblacion, tamano_individuo, generaciones)
print("\nMejor estrategia de operación final:", mejor_individuo[0]) 
 