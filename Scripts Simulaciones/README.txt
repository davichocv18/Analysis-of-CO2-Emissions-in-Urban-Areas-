# Guía Completa para Ejecutar la Simulación en SUMO

Este documento describe de forma detallada los pasos y la estructura necesaria para correr una simulación en SUMO utilizando los scripts y archivos proporcionados.

## 📂 Estructura de Archivos Necesarios

En la carpeta de trabajo deben encontrarse exactamente los siguientes archivos:

1. `configSumo.sumocfg` → Archivo de configuración principal de SUMO.
2. `mapa.net.xml` → Archivo del mapa de la simulación.
3. `VehicleType.xml` → Definición de los tipos de vehículos utilizados en la simulación.
4. `routes.py` → Script para generar rutas aleatorias.
5. `simulaciones.py` → Script para ejecutar todas las simulaciones generadas.
6. `DataProcessing.py` → Script para procesar los datos obtenidos.
7. `README.txt` → Este documento.

**Nota:** Algunos scripts requieren archivos adicionales generados en el proceso. Por ejemplo, `DataProcessing.py` necesita los archivos de emisiones y `sumoTrace` en la misma carpeta.

---

## 🛠️ Funcionalidad de cada Script

### 1️⃣ `routes.py`
- **Objetivo:** Crear *n* rutas diferentes para la densidad estipulada inicialmente.
- **Características:**
  - Garantiza aleatoriedad gracias a la función `random`.
  - Es **importante configurar** la ruta de `randomTrips.py` y la del archivo `mapa.net.xml`.
- **Archivos que necesita:**
  - `randomTrips.py` (ruta configurada dentro del script).
  - `mapa.net.xml`.

---

### 2️⃣ `simulaciones.py`
- **Objetivo:** Ejecutar todas las rutas generadas por `routes.py`.
- **Archivos que necesita:**
  - Archivos de rutas generadas.
  - `configSumo.sumocfg`.
  - `mapa.net.xml`.
  - `VehicleType.xml`.

---

### 3️⃣ `DataProcessing.py`
- **Objetivo:** Procesar los datos de salida generados por SUMO.
- **Archivos que necesita:**
  - Archivos de emisiones.
  - Archivos `sumoTrace`.
- **Salida esperada:**
  - Un dataset procesado en formato `.csv` listo para análisis.

---

## 📊 Estructura del Dataset Final

El dataset procesado incluye datos de dos fuentes principales: `sumoTrace` y `emissions`.

### **sumoTrace:**
- Densidad vehicular por km².
- Distancia total recorrida.
- Densidad porcentual de cada clase.
- Distancia total recorrida para cada clase.
- Cantidad total de vehículos en la simulación.
- Área total de circulación.

### **emissions:**
- Unidades de CO₂ emitidas (total y por clase).

📌 **Total de columnas:** 20.

---

## ▶️ Cómo Ejecutar la Simulación

### Paso 1: Generar Rutas
```bash
python routes.py
```
Este script creará las rutas necesarias en base a la densidad definida.

### Paso 2: Ejecutar Simulaciones
```bash
python simulaciones.py
```
Se correrán todas las rutas generadas en el paso anterior.

### Paso 3: Procesar Datos
```bash
python DataProcessing.py
```
El script procesará los datos generados y exportará un archivo `.csv` con toda la información procesada.

---

## 📌 Recomendaciones
- Verificar que todas las rutas en los scripts (`routes.py` y `simulaciones.py`) apunten correctamente a sus respectivos archivos.
- Asegurarse de que `randomTrips.py` esté correctamente referenciado y accesible.
- Mantener todos los archivos en la misma carpeta para evitar errores de ruta.

---

✅ ¡Listo! Siguiendo estos pasos tendrás tu simulación completa, con rutas aleatorias, ejecución masiva y procesamiento final de datos.
