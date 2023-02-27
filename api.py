from sudoai.pipeline import Pipeline
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from urllib.parse import unquote
from pysondb import db
from flask_cors import CORS





app = Flask(__name__)
api = Api(app)
CORS(app)

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
        return analyse_dialect_tunisian(unquote(text))


@app.route('/jmx/contact', methods=["POST"])
def post():
    
    database = db.getDb("contact.json")
    data = {
            'name' : request.form.get('name'),
            'email' : request.form.get('email'),
            'msg_subject' : request.form.get('msg_subject'),
            'phone_number' : request.form.get('phone_number'),
            'message' : request.form.get('message')
            }

    
    database.add(data)
    return "success"
    

api.add_resource(Sudoai, '/<text>')
  
if __name__ == '__main__':
    app.run(debug = True)
  