from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# vamos a instanciar la aplicacion
app = Flask(__name__)
# vamos a darle la cadena de conexion
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
# para que no saltern alertas en base datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# vamos a inicializar nuestro sql
db = SQLAlchemy(app)
ma = Marshmallow(app)

# vamos a crear una clase llamda categoria
# Creacion de la tabla Categoria


class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))
    # declaro el constructor

    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp


db.create_all()  # vamos a crear la tabla

# Esquema Categoria


class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')


# Una sola respuesta
categoria_schema = CategoriaSchema()
# Cuando sea muchas respuestas
categorias_schema = CategoriaSchema(many=True)
# GEt


@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)
# GET X ID


@app.route('/categoria/<id>', methods=['GET'])
def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)

 # POST


@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)  # se forza el json
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    nuevo_registro = Categoria(cat_nom, cat_desp)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)
  # PUT


@app.route('/categoria/<id>', methods=['PUT'])
def udpdate_categoria(id):
    actualizarcategoria = Categoria.query.get(id)

    data = request.get_json(force=True)  # se forza el json
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    actualizarcategoria.cat_nom = cat_nom
    actualizarcategoria.cat_desp = cat_desp

    db.session.commit()

    return categoria_schema.jsonify(actualizarcategoria)

# DELETE#######################################


@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminarcategoria = Categoria.query.get(id)
    db.session.delete(eliminarcategoria)
    db.session.commit()
    return categoria_schema.jsonify(eliminarcategoria)
# vamos a inicializar el proyecto
#  mensaje de bienvenida


@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido al tutorial Rest Api python'})


if __name__ == "__main__":

    app.run(debug=True)
