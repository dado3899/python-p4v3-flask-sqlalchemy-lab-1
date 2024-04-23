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

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    # Earthquake.query.filter_by(id = id).first()
    eq = Earthquake.query.filter(Earthquake.id == id).first()
    if eq:
        return eq.to_dict(),200
    else:
        return {
                "message": f"Earthquake {id} not found."
            },404
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    magnitude_eqs = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    r_l = []
    for eq in magnitude_eqs:
        r_l.append(eq.to_dict())
    print(r_l)
    return {
        "count": len(magnitude_eqs),
        "quakes": [eq.to_dict() for eq in magnitude_eqs]
    }, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
