from flask import Flask, request, jsonfy
from models import db, Marca,Color,Latas

app=Flask(__name__)
port=5000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
@app.route('/')
def hello world():
    return 'Hola'

if __name__=='__main__':
    print("Starting server")
    