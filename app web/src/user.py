import uuid
from src.position import Position

# CLASS UTILISATEUR
class USER():
	"""docstring for USER"""
	def __init__(self, id="", city="", min_distance=1, position=Position()):
		self.id = id
		self.city = city
		self.min_distance = min_distance
		self.position = position
		# INITIALISATION DE LA DISTANCE MIN PAR RAPPORT AUX AUTRES UTILISATEURS
		self.previous_min_dist_from_other_users = 10000.0 
		self.is_active=True # SI L UTILISATEUR EST EN DEPLACEMENT
	
	def __str__(self):
		text = "Vos information:"
		text += "\n ville: " + self.city 
		text += "\n distance minimale: " + str(self.min_distance)
		text += "\n position: " + str(self.position)
		return text


	# DEFINTION GETTER ET SETTER DE USER
	def get_uuid(self): return uuid.uuid4().hex[:6].upper()
	def getId(self): return self.id
	def getCity(self): return self.city
	def getPosition(self): return self.position
	def setCity(self, city): self.city = city
	def setUuid(self): self.id = self.get_uuid()
	def setId(self, id): self.id = id
	def setPosition(self, position): self.position=position
	def setMinDistance(self, dist): self.min_distance=dist
	def setIsActive(self, active): self.is_active=active
	def setPreviousMinDistanceFromOtherUsers(self, dist): self.previous_min_dist_from_other_users=dist
	# FONCTION METTANT A JOUR LES INFORMATIONS DE L UTILISATEUR
	def set_info(self, id, city, min_distance, is_active):
		self.setId(id)
		self.setCity(city)
		self.setMinDistance(float(min_distance))
		self.setIsActive(is_active)
		