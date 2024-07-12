from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Latas(db.Model):
    __tablename__ = 'latas'
    id = db.Column(db.Integer, primary_key=True)
    tamanio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    marcas = db.relationship("Marca", backref="lata", lazy=True)
    colores = db.relationship("Color", backref="lata", lazy=True)

class Marca(db.Model):
    __tablename__ = 'marcas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    precio_x_litro = db.Column(db.Integer, nullable=False)
    lata_id = db.Column(db.Integer, db.ForeignKey('latas.id'), nullable=False)

class Color(db.Model):
    __tablename__ = 'colores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    lata_id = db.Column(db.Integer, db.ForeignKey('latas.id'), nullable=False)
