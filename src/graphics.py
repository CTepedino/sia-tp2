import json
import os
import matplotlib.pyplot as plt

# Leer configuración
with open("../config/config_results.json", "r") as config_file:
    config = json.load(config_file)

results_dir = config["results_dir"]
archivos = config["files"]
zoom = config["zoom"]
nombre_salida = config.get("output_filename", "grafico_fitness")
letra_inicio = config.get("tag_start", "C")
letra_fin = config.get("tag_end", "M")

# Directorio de salida
output_dir = "../results_graphics"
os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

plt.figure(figsize=(10, 6))

for archivo in archivos:
    ruta = os.path.join(results_dir, archivo)
    with open(ruta, 'r') as f:
        data = json.load(f)

    # Obtener la etiqueta entre las letras dadas
    try:
        inicio = archivo.index(letra_inicio) + 1
        fin = archivo.index(letra_fin, inicio)
        etiqueta = archivo[inicio:fin-1]
    except ValueError:
        etiqueta = archivo  # fallback si no se encuentra

    generaciones = list(range(1, len(data) + 1))
    plt.plot(generaciones, data, label=etiqueta)

# Título y etiquetas
plt.title("Evolución del Fitness según tipo de Cruza")
plt.xlabel("Generación")
plt.ylabel("Mejor Fitness")
if not zoom:
    plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Guardar gráfico en el nuevo directorio
if not zoom:
    path_salida = os.path.join(output_dir, f"{nombre_salida}.png")
else:
    path_salida = os.path.join(output_dir, f"{nombre_salida}_zoom.png")

plt.savefig(path_salida)
print(f"Gráfico guardado como {path_salida}")
