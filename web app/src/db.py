from mysql.connector import connect
from mysql.connector.errors import InterfaceError
from src.user import USER
from src.position import Position


class DB():
    """Database class for managing Create Read Update Delete Insert operations."""
    def __init__(self, host, db_name,
                 table_name, user_name, user_pwd
                 ):
        """Database class contructor."""
        self.host = host
        self.db_name = db_name
        self.table_name = table_name
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.cursor = None

    def connect(self):
        """Database connector fonction.

        Doesn't work. Connection is lost when setting it to the classe attribute cursor.
        """
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        self.cursor = cursor

    def insert_user_into_db(self, user):
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        sql = f"INSERT INTO {self.db_name}.{self.table_name}(id, city, latitude, \
                longitude) VALUES(%s, %s, %s, %s)"
        vals = (user.id, user.city, str(user.position.lat),
                str(user.position.lng), )
        cursor.execute(sql, vals)
        conn.commit()
        cursor.close()
        conn.close()

    def deleteFromDB(self, id_):
        """Delete a user from the database."""
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        sql = f"DELETE FROM {self.db_name}.{self.table_name} WHERE id=%s"
        vals = (id_,)
        cursor.execute(sql, vals)
        conn.commit()
        cursor.close()
        conn.close()

    def updatePosition(self, user):
        """Update user information into the database"""
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        sql = f"UPDATE {self.db_name}.{self.table_name} set latitude=%s, \
                longitude=%s WHERE id=%s"
        vals = (user.position.lat, user.position.lng, user.id,)
        cursor.execute(sql, vals)
        conn.commit()
        cursor.close()
        conn.close()

    def get_user_by_id(self, id_):
        """Get a user from the database by his ID"""
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.db_name}.{self.table_name} WHERE id=%s"
        vals = (id_,)
        cursor.execute(sql, vals)
        try:
            res = cursor.fetchall()[0]
        except InterfaceError as err:  # SI AUCUNE DONNEE N EST RETOURNE
            res = []
        cursor.close()
        conn.close()
        user = USER(city=res['city'], min_distance=res['min_distance'],
                    position=Position(lat=res['latitude'],
                                      lng=res['longitude']
                                      )
                    )
        user.setId(res['id'])
        return user

    def getUsersSameCity(self, city):
        """Get the users form the same city in the database"""
        conn = connect(host=self.host, user=self.user_name,
                       passwd=self.user_pwd, database=self.db_name
                       )
        cursor = conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.db_name}.{self.table_name} WHERE city=%s"
        vals = (city,)
        cursor.execute(sql, vals)
        try:
            users_same_city = cursor.fetchall()
        except InterfaceError as err:  # SI AUCUNE DONNEE N EST RETOURNE
            users_same_city = []
        cursor.close()
        conn.close()
        return users_same_city
