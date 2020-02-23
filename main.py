from flask import Flask, render_template, jsonify, request
from flask_restful import Api, Resource, reqparse
import requests
import json
import geojson
from geojson import Feature, Point, FeatureCollection

from pprint import pprint

# import pdb; pdb.set_trace()

app = Flask(__name__)
api = Api(app)


@app.route('/')
def display_home_page():
    server_base_url = request.base_url
    if '0.0.0.0' not in request.base_url and 'localhost' not in request.base_url:
        # print('not local')
        server_base_url = request.base_url.replace('http://', 'https://')

    return render_template('index.html', lat=45, lng=65, base_url=server_base_url)


@app.route('/api/<lat>/<lng>')
def get_nearby_wikipedia(lat, lng):
    # print('http://api.geonames.org/findNearbyWikipedia?lat=' + lat + '&lng=' + lng + '&username=dillonchaffey')
    response = requests.get(
        'http://api.geonames.org/findNearbyWikipedia?lat=' + lat + '&lng=' + lng + '&username=dillonchaffey')

    from xml.etree.ElementTree import fromstring, ElementTree
    tree = ElementTree(fromstring(response.text))

    geocodeResults = tree.getroot()

    returnArray = []
    for geocodeResult in geocodeResults:
        returnArray.append([
        geocodeResult[1].text,
        geocodeResult[8].text
    ])

   # pprint(returnArray)
    return jsonify(returnArray)


@app.route('/api/buses')
def get_buses():
    # response = requests.get('https://kbus.doublemap.com/map/v2/buses');
    # buses = json.loads(response.text)
    buses = json.loads(
        '[{"id":11,"name":"59","lat":45.0709,"lon":-64.54762,"heading":328,"route":66,"lastStop":1748,"fields":{},"bus_type":"bus","lastUpdate":1582415938}]')

    outBuses = []
    for b in buses:
        outBuses.append(Feature(geometry=Point((b.get('lon'), b.get('lat')))))

    print(geojson.dumps(FeatureCollection(outBuses)))
    print(jsonify(FeatureCollection(outBuses)))
    return jsonify(FeatureCollection(outBuses))


@app.route('/login')
def test_route():
    return jsonify({'test':1})


@app.route('/<lat>/<lng>')
def display_map(lat, lng):
    return render_template('index.html', lat=lat, lng=lng)


if __name__ == '__main__':
    app.run('0.0.0.0', port='8080')