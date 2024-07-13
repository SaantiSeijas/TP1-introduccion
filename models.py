from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Latas(db.Model):
    __tablename__ = 'latas'
    id = db.Column(db.Integer, primary_key=True)
    marca_id = db.Column(db.Integer, db.ForeignKey('marcas.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('colores.id'), nullable=False)
    tamanio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)

        # Relaciones
    marca = db.relationship('Marca', backref='latas')
    color = db.relationship('Color', backref='latas')

    def __init__(self, marca_id, color_id, tamanio):
        self.marca_id = marca_id
        self.color_id = color_id
        self.tamanio = tamanio
        self.precio = tamanio * Marca.query.get(marca_id).precio_x_litro

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_x_litro = db.Column(db.Integer, nullable=False)

class Color(db.Model):
    __tablename__ = 'colores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
