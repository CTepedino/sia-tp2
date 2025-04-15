import json
import os
import matplotlib.pyplot as plt

# Leer configuración
with open("../config/config_results_dir.json", "r") as config_file:
    config = json.load(config_file)

dirs = config["dirs"]
filename = config["filename"]
zoom = config.get("zoom", False)
nombre_salida = config.get("output_filename", "grafico_fitness")

# Directorio de salida
output_dir = "../results_graphics"
os.makedirs(output_dir, exist_ok=True)  # Crea el directorio si no existe

plt.figure(figsize=(10, 6))

for dir_path in dirs:
    json_path = os.path.join(dir_path, filename)

    if not os.path.exists(json_path):
        print(f"❌ Archivo no encontrado: {json_path}")
        continue

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Etiqueta: última parte del path del directorio
    etiqueta = os.path.basename(dir_path)

    generaciones = list(range(1, len(data) + 1))
    plt.plot(generaciones, data, label=etiqueta)

# Título y etiquetas
plt.title("Evolución del Fitness")
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
print(f"✅ Gráfico guardado como {path_salida}")
