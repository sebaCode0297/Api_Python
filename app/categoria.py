# from crypt import methods
# from crypt import methods
from unittest import result
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import true

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/bdpythonapi'
# Con esta declaracion evitares que nos aparezcan alertas o warnming inecesarios.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;

#
db = SQLAlchemy(app);
ma = Marshmallow(app);

# Cracion de una class para crear la tabla cateogia
class Categoria(db.Model):
     cat_id = db.Column(db.Integer, primary_key = True);
     cat_nom = db.Column(db.String(255), nullable = False);
     cat_desp = db.Column(db.String(255), nullable = False);

     def __init__(self, cat_nom, cat_desp):
          self.cat_nom = cat_nom;
          self.cat_desp = cat_desp;

# Funcion para crear la tabla
db.create_all();

# Creacion de esquema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
     fields = ('cat_id','cat_nom','cat_desp');

# Una sola respuesta
categoria_schema = CategoriaSchema();

# Cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many = True);

# Metodo GET por ID
@app.route('/categoria/<id>', methods = ['GET'])
def get_categoria_x_id(id):
     una_categoria = Categoria.query.get(id)
     return categoria_schema.jsonify(una_categoria);
####################################################

# Metodo GET para muchas respuestas
@app.route('/categoria', methods = ['GET'])
def get_categoria():
     all_categoria = Categoria.query.all();
     result =categorias_schema.dump(all_categoria);
     return jsonify(result);
####################################################


# Metodo POST para crear un recurso hacia la bd
@app.route('/categoria', methods = ['POST'])
def insert_categoria():
     data = request.get_json(force = True)
     cat_nom = data['cat_nom']
     cat_desp = data['cat_desp']

     nuevaCategoria = Categoria(cat_nom, cat_desp)

     db.session.add(nuevaCategoria)
     db.session.commit()
     return categoria_schema.jsonify(nuevaCategoria);
####################################################

# Metodo PUT
@app.route('/categoria/<id>', methods = ['PUT'])
def update_categoria(id):
     actualizarcategoria = Categoria.query.get(id);

     data = request.get_json(force = True)
     cat_nom = data['cat_nom']
     cat_desp = data['cat_desp']

     actualizarcategoria.cat_nom = cat_nom;
     actualizarcategoria.cat_desp = cat_desp;

     db.session.commit();
     return categoria_schema.jsonify(actualizarcategoria);
####################################################

# Metodo Delete
@app.route('/categoria/<id>', methods = ['DELETE'])
def delete_categoria(id):
     eliminarCategoria = Categoria.query.get(id)
     db.session.delete(eliminarCategoria);
     db.session.commit();
     return categoria_schema.jsonify(eliminarCategoria);
####################################################


# Iniciacion del servidor
@app.route('/', methods = ['GET'])
def index():
     return jsonify({'status: 200': 'ok upServer'})

if __name__ == '__main__':
     app.run(debug = True)
