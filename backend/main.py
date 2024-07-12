from flask import Flask, request, jsonify
from models import db, Latas, Marca, Color

app=Flask(__name__)
port=5000

app.comfig['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:123456@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def home():
    return 'Hola como estas?'

app.route('latas', methods['GET'])
def get_latas():
    try:
        latas=Latas.query.all()
        latas_data=[]
        for lata in latas:
            lata_data={
                'id':lata.id,
                'tamanio':lata.tamanio,
                'precio':lata.precio,
                'marcas':[],
                'colores':[]
            }
            for marca in lata.marcas:
                marca_data={
                    'id':marca.id,
                    'nombre':marca.nombre
                }
            for color in lata.colores:
                color_data={
                    'id':color.id,
                    'nombre':color.nombre
                }
                lata_data['marcas'].append(marca_data)
                lata_data['colores'].append(color_data)
            latas_data.append(lata_data)
        return jsonify({'latas':latas_data})
    except Exception as error:
        print("Error",error)
        return jsonify({'message':'Internal server error'}),500





if __name__=='__main__':
    app.run(port=8000, debug=True)