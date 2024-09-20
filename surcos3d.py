import librosa
import bpy
import numpy as np
import os
import sys

|
# Asegurarse de que se ha pasado un archivo de audio como argumento
if len(sys.argv) < 2:
    print("Uso: python script.py <ruta_audio>")
    sys.exit(1)

audio_file = sys.argv[1]


# Verificar la ruta del archivo de audio
audio_file = os.path.join(os.path.dirname(__file__), 'musica.mp3')
if not os.path.exists(audio_file):
    raise FileNotFoundError(f"El archivo {audio_file} no existe. Por favor, asegúrate de proporcionar la ruta correcta.")

# Duración mínima del audio en segundos
min_duration = 3

# Cargar el archivo de audio
try:
    print(f"Cargando archivo de audio: {audio_file}")
    y, sr = librosa.load(audio_file, sr=44100)  # Carga el archivo de audio a 44.1kHz
    print(f"Archivo de audio cargado con {len(y)} muestras a {sr} Hz")
except Exception as e:
    raise Exception(f"Error al cargar el archivo de audio: {e}")

# Asegurar que el audio tenga al menos 3 segundos de duración
min_samples = min_duration * sr  # Muestras necesarias para 3 segundos
if len(y) < min_samples:
    print("El audio es demasiado corto, extendiendo la duración...")
    repeat_factor = int(np.ceil(min_samples / len(y)))
    y = np.tile(y, repeat_factor)[:min_samples]  # Repetir el audio hasta alcanzar la duración mínima

# Eliminar el cubo predeterminado si está presente
if "Cube" in bpy.data.objects:
    bpy.data.objects["Cube"].select_set(True)
    bpy.ops.object.delete()  # Eliminar cubo
    print("Eliminando cubo predeterminado...")

# Crear una espiral en Blender en un plano horizontal
def create_spiral(num_turns, radius):
    print(f"Creando espiral con {num_turns} vueltas y radio {radius}")
    curve_data = bpy.data.curves.new(name='spiral', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('POLY')
    num_points = num_turns * 100
    spline.points.add(num_points - 1)
    
    for i, point in enumerate(spline.points):
        angle = 2 * np.pi * (i / 100)  # Calcular el ángulo
        distance = radius + (i / num_points) * radius  # Calcular la distancia radial
        point.co = (distance * np.cos(angle), distance * np.sin(angle), 0, 1)  # Mantener z = 0
    
    curve_obj = bpy.data.objects.new('Curva_Bezier', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    return curve_obj

# Modulación de la espiral con los datos de audio
def modulate_spiral(curve, audio_data, sample_rate):
    print("Modulando espiral con los datos del audio...")
    num_points = len(curve.data.splines[0].points)
    
    # Remuestrear el audio para ajustarlo al número de puntos de la espiral
    audio_resampled = np.interp(np.linspace(0, len(audio_data), num_points), np.arange(len(audio_data)), audio_data)
    
    # Aplicar modulación amplificada a la espiral
    for i, point in enumerate(curve.data.splines[0].points):
        modulation = audio_resampled[i] * 0.1  # Aumentar la escala de modulación
        point.co.x += modulation  # Desplazamiento en el eje X
        point.co.y += modulation  # Desplazamiento en el eje Y
    print("Espiral modulada según el audio.")

# Crear la espiral
num_turns = 20  # Aumentar el número de vueltas para tener más puntos
radius = 10  # Radio inicial
spiral_curve = create_spiral(num_turns, radius)

# Modificar la espiral según los datos de audio
modulate_spiral(spiral_curve, y, sr)

# Convertir la curva en malla para exportar
try:
    bpy.ops.object.select_all(action='DESELECT')
    spiral_curve.select_set(True)
    bpy.context.view_layer.objects.active = spiral_curve
    bpy.ops.object.convert(target='MESH')
    print("Curva convertida en malla.")
except Exception as e:
    raise Exception(f"Error al convertir la curva en malla: {e}")

# Exportar la espiral como un archivo OBJ
export_path = os.path.join(os.path.dirname(audio_file), 'espiral.obj')
try:
    bpy.ops.export_scene.obj(filepath=export_path)
    print(f"Exportando espiral a {export_path}")
except Exception as e:
    raise Exception(f"Error al exportar la espiral como OBJ: {e}")

# Ajustar la cámara y la luz para el renderizado
try:
    camera = bpy.data.objects["Camera"]
    camera.location = (0, -30, 10)
    camera.rotation_euler = (np.radians(75), 0, np.radians(180))
    print("Ajustando la posición de la cámara...")

    light = bpy.data.objects["Light"]
    light.location = (0, -10, 20)
    print("Ajustando la luz...")
except KeyError as e:
    raise Exception(f"No se encontró el objeto de cámara o luz: {e}")

# Renderizar la escena
render_path = os.path.join(os.path.dirname(audio_file), 'imagen.png')
try:
    bpy.context.scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    print(f"Renderizado completo. Imagen guardada en {render_path}")
except Exception as e:
    raise Exception(f"Error al renderizar la imagen: {e}")
