from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Latas, Marca, Color

app = Flask(__name__)
port=5000

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:postgres@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    latas = Latas.query.all()
    return render_template('index.html', latas=latas)

@app.route('/lata/<int:id>')
def lata_detail(id):
    lata = Latas.query.get_or_404(id)
    return render_template('lata.html', lata=lata)


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
                'marcas': [],
                'colores': []
            }
            for marca in lata.marcas:
                marca_data = {
                    'id': marca.id,
                    'nombre': marca.nombre
                }
                lata_data['marcas'].append(marca_data)
            for color in lata.colores:
                color_data = {
                    'id': color.id,
                    'nombre': color.nombre
                }
                lata_data['colores'].append(color_data)
            latas_data.append(lata_data)
        return jsonify({'latas': latas_data})
    except Exception as error:
        print("Error", error)
        return jsonify({'message': 'Internal server error'}), 500
        print("Error",error)
        return jsonify({'message':'Internal server error'}),500



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)