import os
import subprocess
import time
import psutil  # Para medir recursos del sistema

def main():
    num_rutas = int(input("Ingrese la cantidad de rutas disponibles: "))

    sumo_config_template = "configSumo.sumocfg"
    sumo_executable = "sumo"  # Usa "sumo-gui" si quieres visualización

    for i in range(1, num_rutas + 1):
        print(f"\n--- Ejecutando simulación para ruta {i} ---")

        # Crear archivo de configuración .sumocfg específico para esta simulación
        sumo_config = f"sumoConfig_{i}.sumocfg"
        with open(sumo_config_template, "r") as template:
            config_content = template.read()
        config_content = config_content.replace("{i}", str(i))
        with open(sumo_config, "w") as config_file:
            config_file.write(config_content)

        # Iniciar medición de tiempo
        start_time = time.time()

        try:
            # Lanzar proceso SUMO
            process = subprocess.Popen([sumo_executable, "-c", sumo_config])
            child = psutil.Process(process.pid)

            # Medir pico de uso de memoria del proceso hijo
            peak_mem = 0
            while process.poll() is None:
                try:
                    mem = child.memory_info().rss
                    peak_mem = max(peak_mem, mem)
                except psutil.NoSuchProcess:
                    break
                time.sleep(0.1)  # Espera corta para no sobrecargar CPU

            process.wait()
            elapsed_time = time.time() - start_time

            # Reportar recursos
            print(f"✅ Simulación {i} completada.")
            print(f"⏱ Tiempo total: {elapsed_time:.2f} segundos")
            print(f"🔼 Memoria pico usada por SUMO: {peak_mem / (1024 ** 2):.2f} MB")
            print(f"🧵 Núcleos disponibles: {psutil.cpu_count(logical=True)}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error durante la simulación {i}: {e}")
            break

        # Eliminar archivo temporal de configuración
        os.remove(sumo_config)

if __name__ == "__main__":
    main()
