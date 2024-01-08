# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake_route(id):
    database_earthquake = Earthquake.query.filter_by(id = id).first()
    # Earthquake.query.filter_by(id = 1)
    if database_earthquake:
        dict_eq = database_earthquake.to_dict()
        print(dict_eq)
        return make_response(dict_eq,200)
    else:
        return make_response({
                "message": f"Earthquake {id} not found."
            }, 404)
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    eq_list = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    dict_list = []
    for eq in eq_list:
        dict_list.append(eq.to_dict())

    return make_response({
        "count": len(dict_list),
        "quakes": dict_list
    }, 200) 

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
    
