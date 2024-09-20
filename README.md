```markdown
# Proyecto Surcos 3D a Audio

Este proyecto convierte una canción en una representación geométrica de surcos (como en un disco de vinilo) y luego reconvierte esa geometría en una señal de audio. Se asegura que la señal de salida tenga al menos una duración mínima de 3 segundos y permite exportar los resultados en formato `.wav`.

## Requisitos
Asegúrate de tener instaladas las siguientes dependencias. Puedes instalar todas con el archivo `requirements.txt` incluido:

```
numpy
librosa
scipy
```

Además, necesitarás tener Blender instalado para ejecutar los scripts que generan las geometrías en 3D.

## Instrucciones

### Paso 1: Crear y Activar el Entorno Virtual

Un entorno virtual en Python permite aislar las dependencias del proyecto para evitar conflictos entre diferentes proyectos.

#### Instalación del Entorno Virtual

Si no tienes `virtualenv` instalado, puedes hacerlo ejecutando el siguiente comando:

```bash
pip install virtualenv
```

#### Crear el Entorno Virtual

Una vez instalado, crea un entorno virtual para el proyecto. Estando en el directorio raíz del proyecto, ejecuta:

```bash
virtualenv envSurcos
```

Esto creará un directorio llamado `envSurcos` que contendrá los archivos del entorno virtual.

#### Activar el Entorno Virtual

Para activar el entorno virtual, ejecuta el siguiente comando:

En macOS y Linux:
```bash
source envSurcos/bin/activate
```

En Windows:
```bash
envSurcos\Scripts\activate
```

Cuando el entorno virtual está activado, verás que el prefijo `(envSurcos)` aparece al inicio de la línea de tu terminal. Esto indica que ahora estás usando el entorno virtual y todas las dependencias se instalarán en él, sin afectar tu sistema global.

#### Instalar Dependencias

Con el entorno virtual activado, instala las dependencias del proyecto ejecutando:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias para ejecutar el proyecto.

### Paso 2: Análisis de la Canción y Generación de la Espiral en Blender

El siguiente script se utiliza para analizar una canción, convertirla a geometría de surcos (como en un disco de vinilo) y renderizarla en Blender. Asegúrate de tener Blender instalado y configurado correctamente antes de proceder.

#### Ejecución y Renderizado de la Espiral

Para ejecutar Blender desde la línea de comandos y generar la geometría de la espiral, sigue estos pasos:

1. Coloca el archivo de audio que deseas analizar en la raíz del proyecto con el nombre `musica.mp3`.
2. Abre la terminal en el directorio del proyecto y ejecuta el siguiente comando:

```bash
blender --background --python surcos3d.py
```

Este comando ejecutará el script `surcos3d.py`, que analizará la canción y generará una espiral en Blender basada en los datos del audio. Luego, exportará la espiral generada como un archivo OBJ y también realizará un renderizado en formato de imagen.

### Paso 3: Conversión de la Geometría de la Espiral a Audio

Una vez que se haya generado la espiral 3D, el siguiente paso es reconvertir esa geometría en una señal de audio. Esto se hace con el siguiente script.

#### Script para Conversión 3D a Audio

Este script toma el archivo OBJ 3D generado en el paso anterior y convierte los vértices de la espiral en una señal de audio. Se asegura de que la señal tenga al menos 3 segundos de duración.

##### Estructura del Script

- **Verificación de la existencia del archivo OBJ**: Si no se encuentra el archivo, se lanza un mensaje de error claro.
- **Procesamiento de los vértices**: Se leen los vértices del archivo OBJ y se convierten en una señal de audio modulada.
- **Excepciones claras**: El script maneja los errores más comunes, como archivos faltantes o problemas al escribir el archivo de salida.

```python
import os
import numpy as np
import librosa
import scipy.io.wavfile as wav
from scipy.signal import resample

# Asegurar que el archivo OBJ existe
obj_filepath = "./espiral.obj"  # Ruta al archivo OBJ generado en el paso anterior
wav_output = "./Audio.wav"       # Ruta para el archivo de salida de audio

if not os.path.exists(obj_filepath):
    raise FileNotFoundError(f"El archivo {obj_filepath} no existe. Por favor, asegúrate de que la espiral fue generada correctamente.")

# Cargar los vértices desde el archivo OBJ
def load_vertices_from_obj(filepath):
    vertices = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('v '):  # Las líneas de vértices comienzan con 'v'
                    _, x, y, z = line.split()
                    vertices.append((float(x), float(y), float(z)))
        return np.array(vertices)
    except Exception as e:
        raise Exception(f"Error al cargar los vértices desde el archivo OBJ: {e}")

# Convertir las variaciones geométricas a una señal de audio
def vertices_to_audio(vertices, sr=44100, min_duration=3):
    try:
        z_values = vertices[:, 2]  # Extraer el eje Z como modulación de amplitud
        z_normalized = (z_values - np.min(z_values)) / (np.max(z_values) - np.min(z_values))  # Normalizar
        audio_signal = (z_normalized - 0.5) * 2  # Escalar al rango [-1, 1]

        # Suavizado de la señal para evitar saltos bruscos
        smoothed_signal = np.convolve(audio_signal, np.ones(10)/10, mode='same')

        # Asegurar duración mínima
        target_length = sr * min_duration
        if len(smoothed_signal) < target_length:
            audio_signal = resample(smoothed_signal, target_length)
        elif len(smoothed_signal) > target_length:
            audio_signal = smoothed_signal[:target_length]

        return audio_signal
    except Exception as e:
        raise Exception(f"Error al convertir los vértices a una señal de audio: {e}")

# Guardar como archivo de audio
def save_as_wav(signal, sr, filepath):
    try:
        scaled_signal = np.int16(signal * 32767)
        wav.write(filepath, sr, scaled_signal)
        print(f"Audio guardado en {filepath}")
    except Exception as e:
        raise Exception(f"Error al guardar el archivo de audio: {e}")

# Ejecutar el proceso
try:
    vertices = load_vertices_from_obj(obj_filepath)
    audio_signal = vertices_to_audio(vertices)
    save_as_wav(audio_signal, 44100, wav_output)
except FileNotFoundError as fnf_error:
    print(fnf_error)
except Exception as e:
    print(f"Se ha producido un error: {e}")
```

#### Exportar el Audio

El archivo de audio generado se guardará como `Audio.wav` en la raíz del proyecto. Si hay algún problema con la ruta o el archivo de salida, se mostrará un error claro.
```
