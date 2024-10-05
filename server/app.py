#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>',200

@app.route('/heroes')
def get_heroes():
    heroes=Hero.query.all()
    return [hero.to_dict() for hero in heroes],200

@app.route('/heroes/<int:id>')
def get_hero(id):
    hero=Hero.query.filter_by(id=id).first()
    if hero:
        hero_powers=HeroPower.query.filter_by(hero_id=id).all()
        hero=hero.to_dict()
        hero["hero_powers"]=[hero_power.to_dict() for hero_power in hero_powers]
        return hero,200
    else:
        return {"error": "Hero not found"},404

@app.route('/powers')
def get_powers():
    powers=Power.query.all()
    return [power.to_dict() for power in powers]

@app.route('/powers/<int:id>',methods=['GET',"PATCH"])
def get_power(id):
    power=Power.query.filter_by(id=id).first()
    if power:
        if request.method=="GET":
            return power.to_dict(),200
        if request.method=="PATCH":
            data = request.get_json()
            # for attr in request.form:
            #     setattr(power, attr, request.form.get(attr))
            description=data.get('description')
            if len(description)<20:
                return {"errors":["validation errors"]},400
            else:
                power.description=description
            try:
                # db.session.add(power)
                db.session.commit()
                return power.to_dict(),200
            except:
                return {
                    "errors":["validation errors"]
                },400
    else:
        return {"error": "Power not found"},404
    
@app.route('/hero_powers',methods=['POST'])
def post_power():
    data = request.get_json()
    if data['strength'] not in ["Strong","Weak","Average"]:
        return {
            "errors":["validation errors"]
        },400
    new_power=HeroPower(
        strength=data['strength'],
        power_id=data['power_id'],
        hero_id=data['hero_id']
    )
    try:
        db.session.add(new_power)
        db.session.commit()
        return new_power.to_dict(),200
    except:
        return {
            "errors":["validation errors"]
        }



if __name__ == '__main__':
    app.run(port=5555, debug=True)
