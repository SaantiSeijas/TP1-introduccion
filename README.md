# Inventario de Pinturería

Este es un proyecto de gestión de inventario para una pinturería, desarrollado con Flask y PostgreSQL. La aplicación permite administrar marcas de pintura y sus respectivas latas, incluyendo funcionalidades para agregar, modificar y eliminar marcas. Ademas, se puede agregar y eliminar latas

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)


## Características

- Listar marcas y latas.
- Agregar, modificar y eliminar marcas.
- Agregar y eliminar latas.
- Validación de datos en el cliente y el servidor.
- Interfaz de usuario en modo oscuro.

## Tecnologías

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: HTML, CSS (modo oscuro)
- **Base de Datos**: PostgreSQL

## Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL

### Paso a Paso

1. **Clonar el repositorio:**

    ```sh
    git clone https://github.com/tu_usuario/inventario-pintureria.git
    cd inventario-pintureria
    ```

2. **Crear un entorno virtual:**

    ```sh
    python3 -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. **Configurar la base de datos:**

    - Crear una base de datos en PostgreSQL:

    ```sql
    CREATE DATABASE inventario_pintureria;
    ```

    - Actualizar las configuraciones de la base de datos en `main.py`:

    ```python
    SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:contraseña@localhost/inventario_pintureria'
    ```

5. **Ejecutar la aplicación:**

    ```sh
    python3 main.py
    ```

    La aplicación estará disponible en `http://127.0.0.1:5000`.

## Uso

### Página Principal

Al ejecutarse 'main.py' se cargara en la tabla 'colores' todos los colores disponibles. En la página principal se listan todas las marcas disponibles junto con su precio por litro.

### Agregar Marca

Rellena el formulario en la página principal para agregar una nueva marca.

### Modificar Marca

Se redirige a un nuevo template, rellena el formulario para modificar una marca existente. La informacion de la marca pre-modificacion estara cargada (por defecto) en los inputs.

### Eliminar Marca

Rellena el formulario en la página principal para eliminar una marca existente.

### Ver Latas de una Marca

Haz clic en una marca para ver todas las latas asociadas a esa marca.

### Agregar Lata

Rellena el formulario en la página de latas para agregar una nueva lata a la marca seleccionada.

### Eliminar Lata

Rellena el formulario en la página de latas para eliminar una lata existente.

## Estructura del Proyecto

```plaintext
inventario-pintureria/
├── models.py
├── main.py
├── templates/
│   ├── index.html
│   ├── latas.html
│   ├── editarmarca.html
├── static/
│   ├── images/
│       └── logo.png