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
def earthquake_by_id(id):
    e_by_id = Earthquake.query.filter(Earthquake.id == id).first()
    if e_by_id:
        return e_by_id.to_dict(), 200
    else:
        return {
            "message": f"Earthquake {id} not found."
        }, 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    # find all that match
    all_e = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    r_list = []
    for e in all_e:
        r_list.append(e.to_dict())
    r_dict = {
        "count": len(all_e),
        "quakes": r_list
    }
    
    return r_dict

# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
