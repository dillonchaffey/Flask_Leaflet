from flask import Flask, render_template, jsonify
app = Flask(__name__)

test_data_array = []

@app.route('/')
def index():
	return render_template('index.html', lat=45, lng=65)

@app.route('/api/<lat>/<lng>') 
def coordinates(lat,lng):
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
  return jsonify({'cordinates': [ lat, lng ]})

@app.route('/<lat>/<lng>') 
def display_map(lat, lng):
	return render_template('index.html', lat=lat,lng=lng)

if __name__ == '__main__':
	app.run('0.0.0.0',8080)