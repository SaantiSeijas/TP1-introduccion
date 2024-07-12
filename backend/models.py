from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Latas(db.model):
    __tablename__='latas'
    id=db.column(db.Integer,primary_key=True)
    marcas=db.relationship("Marca")
    colores=db.relationship("Color")
    tamanio=db.column(db.Integer,nullable=False)
    precio=db.column(db.Integer,nullable=False)

class Marca(db.Model):
    __tablename__='marcas'
    id= db.column(db.Integer, primary_key=True)
    nombre= db.column(db.String(20),nullable=False)

class Color(db.Model):
    __tablename__='colores'
    id=db.column(db.Integer, primary_key=True)
    nombre=db.column(db.String(20),nullable=False)