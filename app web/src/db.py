from mysql.connector import connect
from mysql.connector.errors import InterfaceError
from src.user import USER
from src.position import Position

# CLASS BASE DE DONNEES
class DB(object):
	def __init__(self, host, db_name, table_name, user_name, user_pwd):
		self.host = host
		self.db_name = db_name
		self.table_name = table_name
		self.user_name = user_name
		self.user_pwd = user_pwd
		self.cursor = None

	# NE MARCHE PAS DU AU BUFFER, UNE FOIS CONNECTER LA CONNECTION EST PERDUE
	def connect(self):
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		self.cursor = cursor

	# INSERTION D UN UTILISATEUR DANS LA BASE
	def insert_user_into_db(self, user):
		#self.connect()
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		sql = f"INSERT INTO {self.db_name}.{self.table_name}(id, city, latitude, longitude) VALUES(%s, %s, %s, %s)"
		vals = (user.id, user.city, str(user.position.lat), str(user.position.lng), )
		cursor.execute(sql, vals)
		conn.commit()
		cursor.close()
		conn.close()
	
	# SURPRESSION D UN UTLISATEUR DE LA BASE
	def delete_user_from_db(self, id):
		#self.connect()
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		sql = f"DELETE FROM {self.db_name}.{self.table_name} WHERE id=%s"
		vals = (id,)
		cursor.execute(sql, vals)
		conn.commit()
		cursor.close()
		conn.close()
		print("Sucessfully deleted!")
			

	# MISE A JOUR DE LA POSITION DANS LA BASE
	def update_user_posotion(self, user):
		#self.connect()
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		sql = f"UPDATE {self.db_name}.{self.table_name} set latitude=%s, longitude=%s WHERE id=%s"
		vals = (user.position.lat, user.position.lng, user.id,)
		cursor.execute(sql, vals)
		conn.commit()
		cursor.close()
		conn.close()	


	# OBTENTION D UN UTILISATEUR DE LA BASE AVEC UN ID
	def get_user_by_id(self, id):
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		sql = f"SELECT * FROM {self.db_name}.{self.table_name} WHERE id=%s"
		vals = (id,)
		cursor.execute(sql, vals)
		try:
			res = cursor.fetchall()[0]
		except InterfaceError as err: # SI AUCUNE DONNEE N EST RETOURNE
			res =[]
		cursor.close()
		conn.close()
		user = USER(city=res['city'], min_distance=res['min_distance'], position=Position(lat=res['latitude'], lng=res['longitude']))
		user = user.setId(res['id'])
		return user

	# OBTENTION DES UTILISATEUR DE LA MEME VILLE
	def get_users_same_city(self, city):
		#self.connect()
		conn = connect(host=self.host, user=self.user_name, passwd=self.user_pwd, database=self.db_name)
		cursor = conn.cursor(dictionary=True)
		sql = f"SELECT * FROM {self.db_name}.{self.table_name} WHERE city=%s"
		vals = (city,)
		cursor.execute(sql, vals)
		try:
			users_same_city = cursor.fetchall()	
		except InterfaceError as err: # SI AUCUNE DONNEE N EST RETOURNE
			users_same_city =[]
		
		cursor.close()
		conn.close()
		return users_same_city