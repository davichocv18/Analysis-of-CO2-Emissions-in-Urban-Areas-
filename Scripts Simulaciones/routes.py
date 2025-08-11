import os
import random
import subprocess
import xml.etree.ElementTree as ET
from lxml import etree
import time
import psutil  # <--- Para monitoreo de recursos

# Clase para actualizar el atributo 'depart' en los archivos
class DepartUpdater:
    def __init__(self, files):
        self.files = files

    def update_depart_in_files(self):
        for file in self.files:
            tree = ET.parse(file)
            root = tree.getroot()
            for element in root.findall(".//*[@depart]"):
                element.set('depart', "0.00")
            tree.write(file)
            print(f"Atributo 'depart' actualizado a '0.00' en el archivo {file}")

# Clase para combinar rutas y actualizar IDs
class RouteMerger:
    def __init__(self, input_files, output_file):
        self.input_files = input_files
        self.output_file = output_file

    def merge_files_and_update_ids(self):
        root = etree.Element("routes")
        counter = 0
        for file in self.input_files:
            tree = etree.parse(file)
            for element in tree.getroot():
                if 'id' in element.attrib:
                    element.set('id', str(counter))
                    counter += 1
                root.append(element)
        tree = etree.ElementTree(root)
        tree.write(self.output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print(f"Archivos combinados y IDs actualizados en {self.output_file}")

# Función principal
def main():
    # Solicitar datos al usuario
    densidad = float(input("Ingrese la densidad vehicular (vehículos/km²): "))
    tamanio_mapa = 6.45  # Tamaño del centro histórico
    num_simulaciones = int(input("Ingrese el número total de simulaciones: "))

    total_vehiculos = int(densidad * tamanio_mapa)
    porcentajes = {
        "Motocicletas": 0.2942,
        "Automovil_Kia_Soluto": 0.2893,
        "SUV_Kia_Sonet": 0.1987,
        "Camioneta_Chevrolet_D-Max": 0.1732,
        "Camion_Chevrolet_Serie_NLR": 0.0444,
    }
    vehiculos_por_tipo = {k: int(total_vehiculos * v) for k, v in porcentajes.items()}

    sumo_tool_path = r"C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py"
    red_path = r"C:\Users\DAVICHO\Desktop\Tesis\Experimental\Centro Historico\centro_historico_quito.net.xml"

    for i in range(1, num_simulaciones + 1):
        print(f"\n--- Simulación {i} ---")
        start_time = time.time()
        process = psutil.Process(os.getpid())

        cpu_start = psutil.cpu_percent(interval=None)
        mem_start = process.memory_info().rss  # Bytes de memoria usados al inicio

        archivos_generados = []
        for j, (tipo, cantidad) in enumerate(vehiculos_por_tipo.items(), start=1):
            seed = random.randint(1, 10**6)
            nombre_archivo = f"{tipo}_{i}.rou.xml"
            comando = [
                "python", sumo_tool_path,
                "-n", red_path,
                "-r", nombre_archivo,
                "-e", str(cantidad),
                "--period", "1",
                "--intermediate", "7",
                "--seed", str(seed),
                "--trip-attributes", f"type=\"{tipo}\"",
                "--fringe-factor", "35",
                "--allow-fringe"
            ]
            subprocess.run(comando, check=True)
            archivos_generados.append(nombre_archivo)

        updater = DepartUpdater(archivos_generados)
        updater.update_depart_in_files()

        archivo_salida = f"route{i}.rou.xml"
        merger = RouteMerger(archivos_generados, archivo_salida)
        merger.merge_files_and_update_ids()

        for archivo in archivos_generados:
            os.remove(archivo)

        # Fin de medición de recursos
        elapsed_time = time.time() - start_time
        cpu_end = psutil.cpu_percent(interval=None)
        mem_end = process.memory_info().rss

        print(f"\n⏱ Tiempo de simulación {i}: {elapsed_time:.2f} segundos")
        print(f"🧠 Memoria usada: {(mem_end - mem_start) / (1024 ** 2):.2f} MB")
        print(f"🧮 Uso de CPU al inicio: {cpu_start}%, al final: {cpu_end}%")
        print(f"🧵 Núcleos disponibles: {psutil.cpu_count(logical=True)}\n")

if __name__ == "__main__":
    main()
