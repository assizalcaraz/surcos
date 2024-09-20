```markdown
## Paso 1: Crear y Activar el Entorno Virtual

Un entorno virtual en Python permite aislar las dependencias del proyecto para evitar conflictos entre diferentes proyectos.

### Instalación del Entorno Virtual

Si no tienes `virtualenv` instalado, puedes hacerlo ejecutando el siguiente comando:

```bash
pip install virtualenv
```

### Crear el Entorno Virtual

Una vez instalado, crea un entorno virtual para el proyecto. Estando en el directorio raíz del proyecto, ejecuta:

```bash
virtualenv env
```

Esto creará un directorio llamado `env` que contendrá los archivos del entorno virtual.

### Activar el Entorno Virtual

Para activar el entorno virtual, ejecuta el siguiente comando según tu sistema operativo:

#### En macOS y Linux:
```bash
source env/bin/activate
```

#### En Windows:
```bash
env\Scripts\activate
```

Cuando el entorno virtual está activado, verás que el prefijo `(env)` aparece al inicio de la línea de tu terminal. Esto indica que ahora estás usando el entorno virtual y todas las dependencias se instalarán en él, sin afectar tu sistema global.

### Instalar Dependencias

Con el entorno virtual activado, instala las dependencias del proyecto ejecutando:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias para ejecutar el proyecto.

Luego de activar el entorno virtual y haber instalado las dependencias, puedes proceder a ejecutar el script con Blender (descrito en el Paso 2).
```
