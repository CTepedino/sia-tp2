import json
import os
import matplotlib.pyplot as plt

# Leer configuración
with open("config_results.json", "r") as config_file:
    config = json.load(config_file)

results_dir = config["results_dir"]
archivos = config["files"]
nombre_salida = config.get("output_filename", "grafico_fitness")
letra_inicio = config.get("tag_start", "C")
letra_fin = config.get("tag_end", "M")

plt.figure(figsize=(10, 6))

for archivo in archivos:
    ruta = os.path.join(results_dir, archivo)
    with open(ruta, 'r') as f:
        data = json.load(f)

    # Obtener la etiqueta entre las letras dadas
    try:
        inicio = archivo.index(letra_inicio) + 1
        fin = archivo.index(letra_fin, inicio)
        etiqueta = archivo[inicio:fin]
    except ValueError:
        etiqueta = archivo  # fallback si no se encuentra

    generaciones = list(range(1, len(data) + 1))
    plt.plot(generaciones, data, label=etiqueta)

# Título y etiquetas
plt.title("Evolución del Fitness según tipo de Cruza")
plt.xlabel("Generación")
plt.ylabel("Mejor Fitness")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Guardar gráfico
plt.savefig(f"{nombre_salida}.png")
print(f"Gráfico guardado como {nombre_salida}.png")
