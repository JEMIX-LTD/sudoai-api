from sudoai.pipeline import Pipeline
from flask import Flask
from flask_restful import Resource, Api
from urllib.parse import unquote
from pysondb import db


app = Flask(__name__)
api = Api(app)

def analyse_dialect_tunisian(_input):

    database = db.getDb("db.json")
    lid = Pipeline(id='lid',compressed=True)
    ttd = Pipeline(id='ttd')
    nsfw = Pipeline(id='nsfw',compressed=True)
    sa = Pipeline(id='sa')

    re = ''

    if lid(inputs=_input) == 'aeb':
        r = []
        for x in _input.split(' '):
            trans = ttd(inputs=x)

            r.append( trans)
        re = ' '.join(r)

    else:
        re = _input

    ns = []
    n = {}

    for x in re.split(' '):
        r = nsfw(inputs=x)
        n[x] = r
        ns.append(r)

    ratio = sum('NOTSAFE' in s for s in ns) / len(ns)
    data = {'sa' : sa(inputs=re) , 'r' : ratio , 'nsfw' : n , 'ttd' : re , 'src' : _input }
    database.add(data)
    return data

class Sudoai(Resource):
  
    def post(self,text):
        return analyse_dialect_tunisian(unquote(text)),  201, {'Access-Control-Allow-Origin': '*'}


api.add_resource(Sudoai, '/<text>')
  
if __name__ == '__main__':
    app.run(debug = True)
  