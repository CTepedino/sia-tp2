# Aproximación de Imágenes mediante Algoritmos Genéticos con Triángulos

Este trabajo práctico implementa un algoritmo genético para aproximar imágenes utilizando composiciones de triángulos translúcidos. A lo largo de generaciones, los individuos evolucionan para representar visualmente una imagen objetivo, aplicando técnicas de selección, cruce y mutación.

---

## Requisitos

- Python 3.8 o superior
- uv: gestor de entornos y dependencias ultra rápido (reemplazo de pip/venv)

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
uv run main.py --image_path path/a/la/imagen.jpg
```

---

## Parámetros disponibles

| Parámetro              | Descripción                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| --image_path           | Ruta a la imagen que se desea aproximar (**obligatorio**)                   |
| --num_triangles        | Cantidad de triángulos por individuo (por defecto: 200)                     |
| --pop_size             | Tamaño de la población (por defecto: 30)                                    |
| --num_generations      | Número de generaciones a simular (por defecto: 50)                          |
| --mutation_rate        | Probabilidad de mutación por triángulo (por defecto: 0.1)                   |
| --elite_count          | Cantidad de individuos élite que se conservan por generación (default: 1)   |
| --selection            | Método de selección: elite, ruleta, torneo                                  |
| --crossover            | Método de cruce: one_point, two_points, uniform                             |
| --mutation             | Tipo de mutación: simple, gene, multigen                                    |
| --young_bias           | Si se incluye, activa un sesgo hacia individuos jóvenes en la evolución     |

---

## Ejemplo completo

```bash
uv run main.py \
  --image_path ejemplos/wancho.jpeg \
  --num_triangles 300 \
  --pop_size 50 \
  --num_generations 200 \
  --mutation multigen \
  --mutation_rate 0.2 \
  --selection torneo \
  --crossover two_points \
  --young_bias
```
---

## Salidas generadas

- output_final.png: mejor individuo final generado.
- gen_XXX.png: imagen del mejor individuo cada 5 generaciones.
- evolucion_fitness.png: gráfico del error MSE a lo largo de las generaciones.

---

## Notas técnicas

- Los triángulos se generan con valores aleatorios de color y transparencia (canal alfa).
- Se usa Image.alpha_composite() para respetar correctamente la superposición de triángulos translúcidos.
- Para mejorar el rendimiento, los triángulos se agrupan en bloques de 10 antes de componer.

---

## Autor

Carlos  
Trabajo práctico para la materia Sistemas de Inteligencia Artificial – ITBA
