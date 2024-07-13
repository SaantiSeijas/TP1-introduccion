from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Latas, Marca, Color

app = Flask(__name__)
port=5000

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/marcas/<int:marca_id>')
def mostrar_latas(marca_id):
    marca = Marca.query.get_or_404(marca_id)
    latas = Latas.query.filter_by(marca_id=marca_id).all()
    return render_template('latas.html', marca=marca, latas=latas)


@app.route('/api/marcas', methods=['GET'])
def get_marcas():
    try:
        marcas = Marca.query.all()
        marcas_data = []
        for marca in marcas:
            marca_data = {
                'id': marca.id,
                'nombre': marca.nombre,
                'precio_x_litro': marca.precio_x_litro,
            }
            marcas_data.append(marca_data)
        return jsonify({'marcas': marcas_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/api/latas', methods=['GET'])
def add_lata():
    data = request.get_json()
    try:
        # Buscar ID de la marca
        marca = Marca.query.filter_by(nombre=data['nombre_marca']).first()
        if not marca:
            return jsonify({'message': 'Marca no encontrada'}), 404
        
        # Buscar ID del color
        color = Color.query.filter_by(nombre=data['nombre_color']).first()
        if not color:
            return jsonify({'message': 'Color no encontrado'}), 404
        
        # Crear nueva lata
        nueva_lata = Latas(marca_id=marca.id, color_id=color.id, tamanio=data['tamanio'])
        db.session.add(nueva_lata)
        db.session.commit()
        
        return jsonify({'message': 'Lata agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al agregar la lata', 'error': str(e)}), 500


@app.route('/agregar_lata', methods=['POST'])
def agregar_lata():
    try:
        # Obtener los datos del formulario
        tamanio = int(request.form.get('tamanio'))  # Convertir tamaño a entero
        nombre_color = request.form.get('nombre_color')
        marca_id = int(request.form.get('marca_id'))  # Convertir marca_id a entero


        # Buscar el color por su nombre
        color = Color.query.filter_by(nombre=nombre_color).first()
        if not color:
            return jsonify({'message': 'Color no encontrado'}), 404

        # Crear una nueva lata
        nueva_lata = Latas(marca_id=marca_id, color_id=color.id, tamanio=tamanio)

        # Agregar la nueva lata a la sesión y commit a la base de datos
        db.session.add(nueva_lata)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as error:
        print("Error al agregar lata:", error)
        return jsonify({'message': 'Error al agregar lata'}), 500

        
@app.route('/agregar_marca', methods=['POST'])
def agregar_marca():
    try:

        nombre = request.form.get('nombre')
        precio_x_litro = request.form.get('precio_x_litro')

        nueva_marca = Marca(nombre=nombre, precio_x_litro=precio_x_litro)
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
        
        db.session.delete(marca)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as error:
        print("Error al eliminar marca:", error)
        return jsonify({'message': 'Error al eliminar marca'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=port, debug=True)