from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource, reqparse
import requests

# import pdb; pdb.set_trace()

app = Flask(__name__)
api = Api(app)


@app.route('/')
def display_home_page():
    server_base_url = request.base_url
    if '0.0.0.0' not in request.base_url and 'localhost' not in request.base_url:
        print('not local')
        server_base_url = request.base_url.replace('http', 'https')

    return render_template('index.html', lat=45, lng=65, base_url=server_base_url)


@app.route('/api/<lat>/<lng>')
def coordinates(lat, lng):
    '''
    addresses = session.query(Coordinates)#however you query your db
    all_coods = [] # initialize a list to store your addresses
    for add in addresses:
       address_details = {
       "lat": add.lat,
       "lng": add.lng,
       "title": add.title}
       all_coods.append(address_details)
    '''
    # return jsonify({'cordinates': [ lat, lng ]})
    # g = geocoder.google([ lat, lng ], method='reverse', sensor=False)
    # g2 = geocoder.google('Sydney, NS')
    # print(g2)
    # print(dir(g.response.raw))
    # http://api.geonames.org/findNearbyWikipedia?lat=45&lng=-65&username=dillonchaffey
    # http://api.geonames.org/findNearbyWikipedia?lat=44.860249404613604&lng=-65.02464294433595&username=dillonchaffey
    # g = geocoder.geonames(location=[ lat, lng ], method='findNearbyWikipedia', lat=lat, lng=lng, key='dillonchaffey')

    # g = geocoder.geonames('Sydney, NS', key='dillonchaffey')
    # import pdb; pdb.set_trace()
    print('http://api.geonames.org/findNearbyWikipedia?lat=' + lat + '&lng=' + lng + '&username=dillonchaffey')
    response = requests.get(
        'http://api.geonames.org/findNearbyWikipedia?lat=' + lat + '&lng=' + lng + '&username=dillonchaffey')


#    print(response.text)
    # import pdb; pdb.set_trace()
    # import xml.etree.ElementTree as ET
    # tree = ET.fromstring(response.text)

    from xml.etree.ElementTree import fromstring, ElementTree
    tree = ElementTree(fromstring(response.text))
    #print(response.text)
    # print(dir(tree))
    root = tree.getroot()
    #print(root[0][8].text)
    return jsonify([
        root[0][1].text,
        root[0][8].text
    ])


@app.route('/login')
def test_route():
    return 'test!'


class Position(Resource):
    def get(self, name):
        for position in positions:
            if (name == position["name"]):
                return position, 200
        return "position not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("lat")
        parser.add_argument("lng")
        args = parser.parse_args()

        for position in positions:
            if (name == position["name"]):
                return "position with name {} already exists".format(name), 400

        position = {
            "name": name,
            "lat": args["lat"],
            "lng": args["lng"]
        }
        positions.append(position)
        return position, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("lat")
        parser.add_argument("lng")
        args = parser.parse_args()

        for position in positions:
            if (name == position["name"]):
                position["lat"] = args["lat"]
                position["lng"] = args["lng"]
                return position, 200

        position = {
            "name": name,
            "lat": args["lat"],
            "lng": args["lng"]
        }
        positions.append(position)
        return position, 201

    def delete(self, name):
        global positions
        positions = [
            position for position in positions if position["name"] != name]
        return "{} is deleted.".format(name), 200


api.add_resource(Position, "/position/<string:name>")


@app.route('/<lat>/<lng>')
def display_map(lat, lng):
    return render_template('index.html', lat=lat, lng=lng)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)