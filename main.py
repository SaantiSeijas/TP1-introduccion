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

@app.route('/lata/<int:id>')
def lata_detail(id):
    lata = Latas.query.get_or_404(id)
    return render_template('lata.html', lata=lata)


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
def get_latas():
    try:
        latas = Latas.query.all()
        latas_data = []
        for lata in latas:
            lata_data = {
                'id': lata.id,
                'tamanio': lata.tamanio,
                'precio': lata.precio,
                'marcas': [{'id': marca.id, 'nombre': marca.nombre, 'precio_x_litro': marca.precio_x_litro} for marca in lata.marcas],
                'colores': [{'id': color.id, 'nombre': color.nombre} for color in lata.colores]
            }
            latas_data.append(lata_data)
        return jsonify({'latas': latas_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/agregar_lata', methods=['POST'])
def agregar_lata():
    try:
        # Obtener los datos del formulario
        tamanio = request.form.get('tamanio')
        precio = request.form.get('precio')

        # Crear una nueva lata
        nueva_lata = Latas(tamanio=tamanio, precio=precio)

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
        lata_id = request.form.get('lata_id')
        nombre = request.form.get('nombre')
        precio_x_litro = request.form.get('precio_x_litro')

        nueva_marca = Marca(nombre=nombre, precio_x_litro=precio_x_litro, lata_id=lata_id)
        db.session.add(nueva_marca)
        db.session.commit()

        return redirect(url_for('home'))
    except Exception as error:
        print("Error al agregar marca:", error)
        return jsonify({'message': 'Error al agregar marca'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=port, debug=True)