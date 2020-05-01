from flask import Flask, session, request, jsonify, render_template, url_for, redirect
from flask import current_app as app
import uuid
from src.user import USER 
from src.position import Position
from src.connection_info import *
from src.db import DB
import time
from mysql.connector import IntegrityError
import os

app = Flask(__name__)
app.secret_key= b'G\xd3\x95iW9\x90\x93M\xf0Aa/XUU' # CLE UTILISER POUR ENREGISTRER DES COOKIES

# INSTANCIATION DE LA BASE DE DONNEE
db = DB(host=DB_HOST, db_name=DB_NAME, table_name=TABLE_NAME, user_name=DB_USER_NAME, user_pwd=DB_USER_PASS_WORD)

#with app.test_request_context():
#if "uuid" in session: # INITIALISATION DES WORKERS GUNICORN
#print("INITIALISATION de WORKER")
#user = USER(id=session["uuid"], city=session["city"], min_distance=session["min_distance"])
user = USER() # INITIALISATION PAR DEFAUT


# INDEX DE LA PAGE WEB
@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('index.html')

# FONCTION RECEVANT LES DONNES DU FORMULAIRE DE CONNECTION
@app.route('/connection', methods=['POST', 'GET'])
def connection():
	print("*************CONNECTION****************")
	city = request.form['ville']
	min_distance = request.form['min_distance']
	uuid = request.form["uuid"]
	#session["uuid"] = uuid
	#session["city"] = city
	#session["min_distance"] = min_distance
	user.set_info(uuid, city, min_distance, is_active=True)
	insert_into_DB() # INSERTION DE L UTILISATEUR COURANT DANS LA BASE DE DONNEES
	return jsonify({})

# PAGE AFFICHER LORSQUE LE BOUTTON DEMARRER EST CLIQUE
@app.route('/realtime', methods=["GET", "POST"])
def real_time():
	return render_template("real_time.html")

# FONCTION CALCULANT EN TEMPS RELLES LES DISTANCES 
# DE L UTILISATEUR COURANT PAR RAPPORT AUX AUTRES DE LA MEME VILLE
@app.route('/realtime/start', methods=['GET', 'POST'])
def real_time_start():
	if user.is_active: # SI L UTILISATEUR EST ACTIF (i.e N A PAS CLIQUEE SUR ARRETER) ALORS FAIRE LES CALCULS
		db.update_user_posotion(user) # MISE A JOUR DE LA POSITION DE L UTILISATEUR DANS LA BASE DE DONNEES
		res_users_same_city=db.get_users_same_city(user.city) # OBTENTION DES UTILISATEURS DE LA MEME VILLE
		print("Current ID", user.id)
		print(res_users_same_city)
		distances=compute_distances(user, res_users_same_city) # CALCULS DES DIFFERENTES DISTANCES
		print(distances)
		alert, min_dist=set_alert(user.min_distance, distances) # MISE A JOUR DU STATUS ALERT
		print("MIN DISTANCE:", min_dist)
		response = jsonify({"alert":alert*1, "dist_closest_user":round(min_dist, 2)})
	else: response = jsonify({"dist_closest_user":10000}) # SI L UTILISATEUR N EST PAS ACTIF RETOURNE LA DISTANCE PAR DEFAUT
	return response #  RETOUR DE LA REPONSE CONTENANT LE SIGNAL D ALERT

# FONCTION RECEVANT LES COORDONNEES DE L UTILISATEUR COURANT
@app.route('/realtime/latlng', methods=['GET', 'POST'])
def getLatLngFromJS():
	print("Mise à jour de la position")
	lat = float(request.form['lat'])
	lng = float(request.form['lng'])
	print("Ancienne position", user.position)
	user.setPosition(Position(lat=lat, lng=lng))
	print("Nouvelle position", user.position)
	return jsonify({})

# FONCTION RECEVANT LE SIGNAL D ARRET DES CALCULS
@app.route('/realtime/stop', methods=['POST', 'GET'])
def real_time_stop():
	user.setPreviousMinDistanceFromOtherUsers(10000.0) # MISE A JOUR DE LA DISTANCE MINIAMLE PAR RAPPORT AUX AUTRES UTILISATEURS
	user.setIsActive(False) # L UTILISATEUR N EST PLUS ACTIF
	db.delete_user_from_db(user.id) # SUPPRESSION DE L UTILISATEUR DE LA BASE DE DONNEES
	#session.pop("uuid", None)
	return jsonify({})


def compute_distances(current_user, res_users_same_city):
	distances = []
	for user in res_users_same_city:
		if user["id"] != current_user.id: # SI L UTILISATEUR EST DIFFERENT DU COURANT
			latlng_user = (float(user["latitude"]), float(user["longitude"]))
			dist = current_user.position.gm_distance(latlng_user)
			distances.append(dist)
	return distances


# FONCTION GERANT L INSERTION DE L UTILISATEUR DANS LA BASE
def insert_into_DB():
	failure=True
	try:
		# INSERTION DE L UTILISATEUR DANS LA BASE
		db.insert_user_into_db(user)
		failure=False
	except IntegrityError as err: 
		pass
	return failure

# FONCTION PERMETTANT LA MISE A JOUR DU STATUS D ALERT
def set_alert(current_user_min_distance, distances):
	alert = False
	min_dist = user.previous_min_dist_from_other_users
	if distances != []: 
		min_dist = min(distances)
		user.setPreviousMinDistanceFromOtherUsers(min_dist)
		if min_dist <= current_user_min_distance:alert=True
	return alert, min_dist


if __name__ == "__main__":
	app.run(threaded=True)