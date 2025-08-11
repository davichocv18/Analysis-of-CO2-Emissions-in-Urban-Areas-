import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os
import gc
import time
import tracemalloc  # <- NUEVO: para medir uso de memoria

def procesar_sumo_trace(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []

    for timestep in root.findall('timestep'):
        time_val = float(timestep.get('time'))
        if time_val < 200:
            continue
        for vehicle in timestep.findall('vehicle'):
            data.append({
                'time': time_val,
                'vehicle_id': vehicle.get('id'),
                'x': float(vehicle.get('x')),
                'y': float(vehicle.get('y')),
                'type': vehicle.get('type'),
                'pos': float(vehicle.get('pos'))
            })

    df = pd.DataFrame(data)
    df['type'] = df['type'].replace({
        'Motocicletas': 'Motorcycles',
        'Automovil_Kia_Soluto': 'Automobile',
        'SUV_Kia_Sonet': "SUV",
        'Camioneta_Chevrolet_D-Max': 'Pickup',
        'Camion_Chevrolet_Serie_NLR': 'Truck'
    })

    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()
    area_km2 = ((x_max - x_min) / 1000) * ((y_max - y_min) / 1000)

    df["distance"] = df.groupby("vehicle_id")["pos"].diff().fillna(0).clip(lower=0) / 1000
    df_distancia = (
        df.groupby(["vehicle_id", "type"])["distance"].sum()
        .reset_index()
        .groupby("type")["distance"].sum()
        .reset_index()
        .rename(columns={"distance": "total_distance_km"})
    )

    distancia_total = df_distancia["total_distance_km"].sum()
    cantidad_vehiculos = df['vehicle_id'].nunique()
    distribucion_vehiculos = df['type'].value_counts(normalize=True) * 100

    datos_finales = {
        'Total vehicle density per km2': cantidad_vehiculos / area_km2,
        'Total distance traveled (km)': distancia_total,
        'Total number of vehicles in the simulation': cantidad_vehiculos,
        'Total circulation area (km2)': area_km2
    }

    for tipo, porcentaje in distribucion_vehiculos.items():
        datos_finales[f'Percentage {tipo}'] = porcentaje

    for _, row in df_distancia.iterrows():
        datos_finales[f'Distance traveled by {row["type"]} (km)'] = row['total_distance_km']

    return pd.DataFrame([datos_finales])

def ewma_iterative(theta, b):
    result = []
    smoothed_value = 0
    for i, value in enumerate(theta):
        smoothed_value = b * smoothed_value + (1 - b) * value
        result.append(smoothed_value)
    return result

def apply_ewma_bias_corr(data, b=0.90):
    v_data = []
    for i in np.arange(1, len(data) + 1):
        v_data.append(ewma_iterative(data[:i], b=b)[-1] / (1 - b**i))
    return v_data

def procesar_emissions(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []

    for timestep in root.findall(".//timestep"):
        time_val = float(timestep.get('time'))
        if time_val < 200:
            continue
        for vehicle in timestep.findall('vehicle'):
            data.append({
                'time': time_val - 200,
                'type': vehicle.get('type'),
                'id': vehicle.get('id'),
                'CO2': float(vehicle.get('CO2'))
            })

    df = pd.DataFrame(data)
    df['type'] = df['type'].replace({
        'Motocicletas': 'Motorcycles',
        'Automovil_Kia_Soluto': 'Automobile',
        'SUV_Kia_Sonet': "SUV",
        'Camioneta_Chevrolet_D-Max': 'Pickup',
        'Camion_Chevrolet_Serie_NLR': 'Truck'
    })

    def create_ewma_dataset(df, b=0.90):
        ewma_results = []
        vehicle_ids = df["id"].unique()
        for vehicle_id in vehicle_ids:
            df_filtered = df[df["id"] == vehicle_id]
            smoothed_co2 = apply_ewma_bias_corr(list(df_filtered["CO2"]), b=b)
            ewma_results.append(pd.DataFrame({
                "time": df_filtered["time"].values,
                "type": df_filtered["type"].values,
                "id": vehicle_id,
                "CO2": smoothed_co2
            }))
        return pd.concat(ewma_results, ignore_index=True)

    df_ewma = create_ewma_dataset(df, b=0.90)
    mean_co2_per_vehicle = df_ewma.groupby(["type", "id"])['CO2'].mean()
    total_mean_co2_by_type = mean_co2_per_vehicle.groupby("type").sum()

    results = {f"Units of CO2 emitted by {vehicle_type}": co2_value for vehicle_type, co2_value in total_mean_co2_by_type.items()}
    results["total units of CO2 emitted"] = total_mean_co2_by_type.sum()

    return pd.DataFrame([results])

if __name__ == "__main__":
    num_archivos = int(input("Ingrese la cantidad de archivos a procesar: "))
    dataset_csv = "dataset.csv"
    df_final = pd.DataFrame()

    for i in range(1, num_archivos + 1):
        print(f"\n--- Procesando simulación {i} ---")
        
        # Iniciar medición
        start_time = time.time()
        tracemalloc.start()

        sumo_path = f"sumoTrace_{i}.xml"
        emissions_path = f"emissions_{i}.xml"

        df_sumo = procesar_sumo_trace(sumo_path) if os.path.exists(sumo_path) else pd.DataFrame()
        gc.collect()

        df_emissions = procesar_emissions(emissions_path) if os.path.exists(emissions_path) else pd.DataFrame()
        gc.collect()

        df_resultado = pd.concat([df_sumo, df_emissions], axis=1) if not df_sumo.empty and not df_emissions.empty else pd.DataFrame()
        df_final = pd.concat([df_final, df_resultado], ignore_index=True)
        gc.collect()

        # Finalizar medición
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        elapsed_time = time.time() - start_time
        tracemalloc.stop()

        print(f"⏱ Tiempo de procesamiento: {elapsed_time:.2f} segundos")
        print(f"🔼 Memoria pico usada (tracemalloc): {peak_mem / (1024**2):.2f} MB")

        del df_sumo, df_emissions, df_resultado

    if not df_final.empty:
        df_final.to_csv(dataset_csv, index=False)
        print(f"\n✅ Resultados guardados en {dataset_csv}")
    else:
        print("⚠️ No se procesaron archivos válidos.")
