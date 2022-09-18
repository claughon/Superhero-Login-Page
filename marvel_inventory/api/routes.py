from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, Superhero, hero_schema, heros_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'name' : 'lando'}

@api.route('/superheros', methods = ['POST'])
@token_required
def create_superhero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_established = request.json['date_established']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token}")

    superhero = Superhero(name, description, comics_appeared_in, super_power, date_established, user_token = user_token )

    db.session.add(superhero)
    db.session.commit()

    response = hero_schema.dump(superhero)

    return jsonify(response)

@api.route('/superheros/<id>', methods = ['GET'])
@token_required
def get_superhero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        superhero = Superhero.query.get(id)
        response = hero_schema.dump(superhero)
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401

@api.route('/superheros', methods = ['GET'])
@token_required
def get_heros(current_user_token):
    owner = current_user_token.token
    heros = Superhero.query.filter_by(user_token = owner).all()
    response = heros_schema.dump(heros)
    return jsonify(response)

@api.route('/superheros/<id>', methods = ['POST', 'PUT'])
@token_required
def update_superhero(current_user_token, id):
    hero = Superhero.query.get(id)

    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.super_power = request.json['super_power']
    hero.date_established = request.json['date_established']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/superheros/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Superhero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)