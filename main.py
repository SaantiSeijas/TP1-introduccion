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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=port, debug=True)