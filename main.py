from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Latas, Marca, Color


app = Flask(__name__)
port=5000


app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

colors = [
    {'nombre': 'rojo'},
    {'nombre': 'verde'},
    {'nombre': 'azul'},
    {'nombre': 'violeta'},
    {'nombre': 'naranja'},
    {'nombre': 'negro'},
    {'nombre': 'blanco'},
    {'nombre': 'marron'},
    {'nombre': 'gris'},
    {'nombre': 'rosa'},
    {'nombre': 'celeste'},
    {'nombre': 'amarillo'},
]


def cargar_colores():
    existing_colors = {color.nombre for color in Color.query.all()}
    new_colors = [Color(**color) for color in colors if color['nombre'] not in existing_colors]

    if new_colors:
        db.session.add_all(new_colors)
        db.session.commit()
        print(f"{len(new_colors)} colores cargados.")
    else:
        print("Todos los colores ya están cargados.")


@app.route('/')
def home():
    marcas = Marca.query.all()
    return render_template('index.html', marcas=marcas)


@app.route('/marcas/<int:marca_id>')
def mostrar_latas(marca_id):
    marca = Marca.query.get_or_404(marca_id)
    latas = Latas.query.filter_by(marca_id=marca_id).all()

    # Calcular la cantidad total de litros y la cantidad total de latas
    total_litros = sum(lata.tamanio for lata in latas)
    total_latas = len(latas)

     # Calcular el precio total de todas las latas de la marca
    total_precio = total_litros * marca.precio_x_litro

    colores_max_litros = []
    litros_max_litros = 0

    if latas:
        # Calcular el color con más litros
        colores = {}
        for lata in latas:
            if lata.color.nombre not in colores:
                colores[lata.color.nombre] = 0
            colores[lata.color.nombre] += lata.tamanio

        max_litros = max(colores.values())
        colores_max_litros = [color for color, litros in colores.items() if litros == max_litros]
        litros_max_litros = max_litros

    color_map = {
        'rojo': 'red',
        'azul': 'blue',
        'verde': 'green',
        'amarillo': 'yellow',
        'negro': 'black',
        'blanco': 'white',
        'gris': 'grey',
        'marron': 'brown',
        'naranja': 'orange',
        'rosa': 'pink',
        'celeste': 'sky blue',
    }

    return render_template('latas.html', marca=marca, latas=latas, total_litros=total_litros, total_latas=total_latas, total_precio=total_precio, colores_max_litros=colores_max_litros, litros_max_litros=litros_max_litros, color_map=color_map)


@app.route('/agregar_lata', methods=['POST'])
def agregar_lata():
    try:
        # Obtener los datos del formulario
        tamanio = int(request.form.get('tamanio'))  # Convertir tamaño a entero
        nombre_color = request.form.get('nombre_color').lower() # Convertir a minúsculas
        marca_id = int(request.form.get('marca_id'))  # Convertir marca_id a entero


        # Buscar el color por su nombre
        color = Color.query.filter_by(nombre=nombre_color).first()
        if not color:
            return jsonify({'message': 'Color no encontrado, por favor ingrese un color existente'}), 404

        # Crear una nueva lata
        nueva_lata = Latas(marca_id=marca_id, color_id=color.id, tamanio=tamanio)

        # Agregar la nueva lata a la sesión y commit a la base de datos
        db.session.add(nueva_lata)
        db.session.commit()

        return redirect(url_for('mostrar_latas', marca_id=marca_id))
    except Exception as error:
        print("Error al agregar lata:", error)
        return jsonify({'message': 'Error al agregar lata'}), 500


@app.route('/eliminar_lata', methods=['POST'])
def eliminar_lata():
    try:
        # Obtener el ID de la lata a eliminar desde el formulario
        lata_id = int(request.form.get('lata_id'))

        # Buscar la lata por su ID en la base de datos
        lata = Latas.query.get(lata_id)
        if not lata:
            return jsonify({'message': 'Lata no encontrada'}), 404

        # Obtener el marca_id antes de eliminar la lata
        marca_id = lata.marca_id

        # Eliminar la lata de la sesión y commit a la base de datos
        db.session.delete(lata)
        db.session.commit()

        return redirect(url_for('mostrar_latas', marca_id=marca_id))
    except Exception as error:
        print("Error al eliminar lata:", error)
        return jsonify({'message': 'Error al eliminar lata'}), 500


@app.route('/agregar_marca', methods=['POST'])
def agregar_marca():
    try:
        nombre = request.form.get('nombre')
        precio_x_litro = request.form.get('precio_x_litro')
        imagen_url = request.form.get('imagen_url')

        nueva_marca = Marca(nombre=nombre, precio_x_litro=precio_x_litro, imagen_url=imagen_url)
        db.session.add(nueva_marca)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as error:
        print("Error al agregar marca:", error)
        return jsonify({'message': 'Error al agregar marca'}), 500


@app.route('/eliminar_marca', methods=['POST'])
def eliminar_marca():
    try:
        nombre = request.form.get('nombre')
        marca = Marca.query.filter_by(nombre=nombre).first()
        if not marca:
            return jsonify({'message': 'Marca no encontrada'}), 404
        
        Latas.query.filter_by(marca_id=marca.id).delete()

        db.session.delete(marca)
        db.session.commit()

        return redirect(url_for('home'))  # Redirige a la página principal
    except Exception as error:
        print("Error al eliminar marca:", error)
        return jsonify({'message': 'Error al eliminar marca'}), 500


@app.route('/editar_marca', methods=['POST'])
def editar_marca():
    try:
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        nuevo_precio_x_litro = float(request.form.get('precio_x_litro'))
        imagen_url = request.form.get('imagen_url')

        # Buscar la marca por su nombre
        marca = Marca.query.filter_by(nombre=nombre).first()
        if not marca:
            return jsonify({'message': 'Marca no encontrada'}), 404

         # Obtener el precio actual por litro
        precio_anterior = marca.precio_x_litro

        # Actualizar los datos de la marca si se proporcionan nuevos valores
        if nuevo_precio_x_litro:
            marca.precio_x_litro = nuevo_precio_x_litro
            
            # Actualizar el precio de las latas de esta marca
            latas = Latas.query.filter_by(marca_id=marca.id).all()
            for lata in latas:
                lata.precio = lata.tamanio * nuevo_precio_x_litro
                
        if imagen_url:
            marca.imagen_url = imagen_url

        # Commit a la base de datos
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as error:
        print("Error al editar marca:", error)
        return jsonify({'message': 'Error al editar marca'}), 500
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        cargar_colores()
    app.run(port=port, debug=True)