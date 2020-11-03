import time
import flask
from flask import Flask
from flask import url_for
from mysql.connector import IntegrityError

from src.user import USER
from src.position import Position
from src import connection_info
from src.db import DB

app = Flask(__name__)
app.secret_key = b'G\xd3\x95iW9\x90\x93M\xf0Aa/XUU'  # CLE UTILISER POUR ENREGISTRER DES COOKIES

db = DB(host=connection_info.DB_HOST,
        db_name=connection_info.DB_NAME,
        table_name=connection_info.TABLE_NAME,
        user_name=connection_info.DB_USER_NAME,
        user_pwd=connection_info.DB_USER_PASS_WORD
        )
user = USER()


@app.route('/', methods=['POST', 'GET'])
def index():
    return flask.render_template('index.html')


@app.route('/connection', methods=['POST', 'GET'])
def connection():
    city = flask.request.form['ville']
    min_distance = flask.request.form['min_distance']
    uuid = flask.request.form["uuid"]
    user.setInfo(uuid, city, min_distance, is_active=True)
    _insertIntoDB()
    return flask.jsonify({})


@app.route('/realtime', methods=["GET", "POST"])
def real_time():
    return flask.render_template("real_time.html")


@app.route('/realtime/start', methods=['GET', 'POST'])
def real_time_start():
    if user.is_active:
        db.updatePosition(user)
        res_users_same_city = db.getUsersSameCity(user.city)
        distances = compute_distances(user, res_users_same_city)
        alert, min_dist = set_alert(user.min_distance, distances)
        response = flask.jsonify(
                                 {"alert": alert*1,
                                  "dist_closest_user": round(min_dist, 2)
                                  }
                                )
    else:
        response = flask.jsonify({"dist_closest_user": 10000})
    return response


@app.route('/realtime/latlng', methods=['GET', 'POST'])
def getLatLngFromJS():
    lat = float(flask.request.form['lat'])
    lng = float(flask.request.form['lng'])
    user.setPosition(Position(lat=lat, lng=lng))
    return flask.jsonify({})


@app.route('/realtime/stop', methods=['POST', 'GET'])
def real_time_stop():
    user.setPreviousMinDistanceFromOtherUsers(10000.0)
    user.setIsActive(False)
    db.deleteFromDB(user.id)
    return flask.jsonify({})


def compute_distances(current_user, res_users_same_city):
    distances = []
    for user in res_users_same_city:
        if user["id"] != current_user.id:
            latlng_user = (float(user["latitude"]), float(user["longitude"]))
            dist = current_user.position.gmDistance(latlng_user)
            distances.append(dist)
    return distances


def _insertIntoDB():
    failure = True
    try:
        db.insert_user_into_db(user)
        failure = False
    except IntegrityError as err:
        pass
    return failure


def set_alert(current_user_min_distance, distances):
    alert = False
    min_dist = user.previous_min_dist_from_other_users
    if distances != []:
        min_dist = min(distances)
        user.setPreviousMinDistanceFromOtherUsers(min_dist)
        if min_dist <= current_user_min_distance:
            alert = True
    return alert, min_dist


if __name__ == "__main__":
    app.run(threaded=True)
