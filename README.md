# Aproximación de Imágenes mediante Algoritmos Genéticos con Triángulos

Este trabajo práctico implementa un algoritmo genético para aproximar imágenes utilizando composiciones de triángulos. A lo largo de generaciones, los individuos evolucionan para representar visualmente una imagen objetivo, aplicando técnicas de selección, cruce y mutación.

---

## Requisitos

- Python 3.8 o superior
- uv: gestor de entornos y dependencias

### Instalación de uv:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### Sincronización de dependencias:

Este proyecto incluye un archivo requirements.txt. Para instalar todo con uv, ejecutar:

```bash
uv venv .venv  
uv sync
```

Esto crea el entorno virtual en .venv e instala automáticamente las dependencias necesarias.

---

## Ejecución

El programa se ejecuta desde consola utilizando uv run:

```bash
uv run main.py config_file_path
```

---

## Archivo de configuración

El programa recibe un archivo de configuración en formato JSON, en el cual se pueden indicar los siguientes parametros:

- image: ubicación de la imagen óbjetivo
- triangle_count: cantidad de triángulos que las recreaciones deben tener
- selection_method: método de selección de individuos
- crossover_method: método de cruza de individuos
- mutation_method: método de mutación de individuos
- generation_method: método de conformación de generaciones
- generation_size: cantidad de individuos por generación
- selected_parents_size: cantidad de padres seleccionados para la cruza por generación
- crossover_probability: probabilidad de cruza
- mutation_probability: probabilidad de mutación
- cut_conditions: especificaciones sobre la/las condiciones de corte a utilizar

  - time: máximo tiempo de ejecución
  - generations: máximo número de generaciones
  - acceptable_solution: valor objetivo de la función de fitness
  - unchanging_individuals: un porcentaje de individuos se mantiene igual a lo largo de un número de generaciones
        
    - threshold: porcentaje minimo de similitud
    - generations: cantidad de generaciones
  - unchanging_max_fitness: cantidad de generaciones en la que se mantiene constante el máximo valor de fitness encontrado

- positional_mutation_range: maxima variación de pixeles que puede tener un vertice de un triángulo al mutar
- color_mutation_range: maxima variación del valor de color que puede tener un triángulo en una mutación
- boltzmann_initial_temperature: valor inicial de la temperatura en el método Boltzmann
- boltzmann_minimum_temperature: minimo valor que puede alcanzar la temperatura en el método Boltzmann
- deterministic_tournament_participants: cantidad de participantes que conformen un torneo determinístico
- probabilistic_tournament_threshold: threshold a usar en el método de torneo probabilístico

## Métodos de selección

Los posibles métodos de selección son los siguientes:

- elite
- roulette
- universal
- ranking
- boltzmann
- deterministic_tournament
- probabilistic_tournament

## Métodos de cruza

- single_point
- double_point
- ring
- uniform

## Métodos de mutación

- gen_mutation
- multigen_mutation
- uniform_mutation
- complete_mutation

## Métodos de conformación de generación

- fill_all
- fill_parent

