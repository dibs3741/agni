from __future__ import print_function
import sys
from flask import Blueprint, jsonify, request, redirect, render_template, url_for, current_app
from flask_restplus import Resource, Api
from project.api.models import User
from project.api.models import cInvestmentModel
from project.api.models import cPosition
from project import db
from sqlalchemy.sql import text
from json import JSONEncoder

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint, prefix = "")

# routes ---
class EqtlJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, cInvestmentModel):
            return {
                   'colAccount'    : obj.account,
                   'colCategory'   : obj.category,
                   'colAllocation' : str(obj.allocation)
            }
        if isinstance(obj, cPosition):
            return {
                   'colAsofDate'     : str(obj.asofdate),
                   'colAccount'      : obj.accname,
                   'colSymbol'       : obj.symbol, 
                   'colCostBasis'    : str(obj.costbasis), 
                   'colCurrentValue' : str(obj.currentvalue)
            }
        return super(EqtlJSONEncoder, self).default(obj)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route("/model/sleeve", methods=['GET'])
def portfolio_model_sleeve():
    dt   = request.args.get('dt')
    acc  = request.args.get('acc')
    cat  = request.args.get('cat')
    file = text(open('./project/sql/getSleeveAllocation.sql', 'r').read())
    d = db.session.execute(file, {"d":dt, "acc":acc, "cat":cat})
    data = []
    for row in d: 
        data.append({
            'colAsofDate'  : str(row['asofdate']),
            'colAccount'   : row['accname'],
            'colCategory'  : row['category'],
            'colSymbol'    : row['symbol'],
            'colAllocation': str(row['ratio']),
            'colActualPct' : str(row['model']),
            'colActual'    : str(row['actual']),
            'colExpected'  : str(row['forecast']),
            'colDifference': str(row['spread'])
        })
    return jsonify(data=data)

@users_blueprint.route("/model", methods=['GET'])
def portfolio_model():
    dt = request.args.get('dt')
    acc = request.args.get('acc')
    file = text(open('./project/sql/getAccountAllocation.sql', 'r').read())
    d = db.session.execute(file, {"d":dt, "acc":acc})
    data = []
    for row in d: 
        data.append({
            'colAsofDate'  : str(row['asofdate']),
            'colAccount'   : row['accname'],
            'colCategory'  : row['category'],
            'colSymbol'    : "",
            'colAllocation': str(row['allocation']),
            'colActualPct' : str(row['actualpercent']),
            'colActual'    : str(row['actual']),
            'colExpected'  : str(row['expected']),
            'colDifference': str(row['difference']) 
        })
    return jsonify(data=data)

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    username = post_data.get('username')
    email = post_data.get('email')
    db.session.add(User(username=username, email=email))
    testval = post_data.get('value')
    db.session.add(User(col1=testval))
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': f'{testval} was added!'
    }
    return jsonify(response_object), 201

class cAllocation(Resource): 
    def get(self): 
        strats = cInvestmentModel.query.all()
        current_app.json_encoder = EqtlJSONEncoder
        return jsonify(data=strats)
api.add_resource(cAllocation, "/allocation", methods=['GET'])

class cGetPosition(Resource): 
    def get(self): 
        dt = request.args.get('dt')
        acc = request.args.get('acc')
        strats = cPosition.query.filter(
            cPosition.asofdate == dt, 
            cPosition.accname == acc
        ).all()
        current_app.json_encoder = EqtlJSONEncoder
        return jsonify(data=strats)
api.add_resource(cGetPosition, "/position", methods=['GET'])

@users_blueprint.route("/navigate", methods=['GET'])
def to_navigate():
    id = request.args.get('id')
    msg = request.args.get('msg')
    #post_data = request.get_json()
    print(msg, file=sys.stderr)
    if 'Model' in msg: 
        return render_template('model.html', user="dibs", topic='Home', env="DEV")
    if 'Position' in msg: 
        return render_template('position.html', user="dibs", topic='Home', env="DEV")
    if 'Allocation' in msg: 
        return render_template('allocation.html', user="dibs", topic='Home', env="DEV")
    return redirect(url_for('users.main'))

@users_blueprint.route("/")
def main():
    return render_template('index.html', user="dibs", topic='Home', env="DEV")

