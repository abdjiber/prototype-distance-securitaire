import googlemaps as gm 

GM_API_KEY = "AIzaSyAcVPFRpZKPgnTv-29eDG1GLkOWEhpDhvw"
gm = gm.Client(key=GM_API_KEY)

# CLASS POSITION
class Position():
	def __init__(self, lat=48.866667, lng=2.333333): # INITIALISATION DE LA POSITION A PARIS
		self.lat = lat
		self.lng = lng
		self.accuracy = 0.0
	
	def __str__(self):
		return f"Latitude: {self.lat}, longitude: {self.lng}"

		
	def gm_distance(self, lat_lng): # RETOURNE LA DISTANCE ENTRE DEUX POINTS EN UTLISANT GOOGLE MAPS
		res = gm.distance_matrix((self.lat, self.lng), (lat_lng))
		dist = self.convertStringToFloatAndMeter(res['rows'][0]['elements'][0]['distance']['text'])
		return dist
	
	def convertStringToFloatAndMeter(self, val): # CONVERTION DE LA DISTANCE RETOURNEE PAR GOOGLE MAPS EN RELLE
		unite_distance = val[-2:]
		if unite_distance == "km": coef_convertion = 1e3
		else: coef_convertion=1
		if "m" in val: val=val.replace("m", "")
		if "k" in val: val=val.replace("k", "")
		if " " in val: val=val.replace(" ", "")
		return float(val)*coef_convertion

	def getCurrentPosition(self): # MISE A JOUR DE LA POSITION AVEC GOOGLE MAPS (NON UTILISER DANS LE PROJET)
		coords = gm.geolocate()
		self.lat = coords['location']['lat']
		self.lng = coords['location']['lng']
		self.accuracy = coords['accuracy'] 
		return self
		
