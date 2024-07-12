from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Marca(db.Model):
    __tablename__='marca'
    id= db.column(db.Integer, primary_key=True)
    nombre= db.column(db.String(20),nullable=False)

class Color(db.Model):
    __tablename__='color'
    id=db.column(db.Integer, primary_key=True)
    nombre=db.column(db.String(20),nullable=False)

class Latas(db.model):
    __tablename__='latas'
    id=db.column(db.Integer,primary_key=True)
    marca_id=db.column(db.Integer, db.ForeignKey('marca.id'))
    color_id=db.column(db.Integer, db.ForeignKey('color.id'))
    tamanio=db.column(db.Integer,nullable=False)
    precio=db.column(db.Integer,nullable=False)



