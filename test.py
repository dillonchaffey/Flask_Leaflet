import requests
import json
import geojson
from geojson import Feature, Point, FeatureCollection


# response = requests.get('https://kbus.doublemap.com/map/v2/buses');
# buses = json.loads(response.text)
buses = json.loads('[{"id":11,"name":"59","lat":45.0709,"lon":-64.54762,"heading":328,"route":66,"lastStop":1748,"fields":{},"bus_type":"bus","lastUpdate":1582415938}]')

outBuses = []
for b in buses:
    outBuses.append(Feature(geometry=Point((b.get('lon'), b.get('lat')))))

print(geojson.dumps(FeatureCollection(outBuses)))