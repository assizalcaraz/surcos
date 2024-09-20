import os
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import resample

# Función para cargar los vértices desde el archivo OBJ
def load_vertices_from_obj(filepath):
    vertices = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Las líneas de vértices comienzan con 'v'
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))
    return np.array(vertices)

# Función para convertir los vértices a señal de audio
def vertices_to_audio(vertices, sr=44100, min_duration=3):
    z_values = vertices[:, 2]  # Extraer el eje Z como modulación de amplitud
    # Normalizar la señal
    z_normalized = (z_values - np.min(z_values)) / (np.max(z_values) - np.min(z_values))
    # Escalar a la amplitud deseada
    audio_signal = (z_normalized - 0.5) * 2  # Dejarla en rango [-1, 1]
    
    # Suavizado de la señal para evitar saltos bruscos
    smoothed_signal = np.convolve(audio_signal, np.ones(10)/10, mode='same')

    # Calcular la cantidad de muestras necesaria para alcanzar la duración mínima
    target_length = sr * min_duration

    # Si la señal es más corta, usar resample para estirarla suavemente
    if len(smoothed_signal) < target_length:
        audio_signal = resample(smoothed_signal, target_length)
    # Si es más larga, cortarla
    elif len(smoothed_signal) > target_length:
        audio_signal = smoothed_signal[:target_length]

    return audio_signal

# Función para guardar la señal de audio en formato WAV
def save_as_wav(signal, sr, filepath):
    # Escalar la señal al rango adecuado para WAV [-32767, 32767] para 16-bit PCM
    scaled_signal = np.int16(signal * 32767)
    wav.write(filepath, sr, scaled_signal)

# Definir la ruta del archivo OBJ y asegurarse de que exista
obj_filepath = os.path.join(os.path.dirname(__file__), 'espiral.obj')

if not os.path.exists(obj_filepath):
    raise FileNotFoundError(f"El archivo {obj_filepath} no existe. Por favor, asegúrate de proporcionar la ruta correcta.")

# Cargar los vértices del archivo OBJ
vertices = load_vertices_from_obj(obj_filepath)

# Convertir los vértices a una señal de audio
audio_signal = vertices_to_audio(vertices)

# Definir la ruta de salida para el archivo de audio WAV
wav_output = os.path.join(os.path.dirname(__file__), 'audio_output.wav')

# Guardar la señal de audio como un archivo WAV
save_as_wav(audio_signal, 44100, wav_output)
print(f"Audio generado a partir del archivo OBJ guardado en {wav_output}")
