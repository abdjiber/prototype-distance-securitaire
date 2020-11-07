from src.position import Position


class USER():
    """Class for managing user."""
    def __init__(self, id_="", city="", min_distance=1, position=Position()):
        self.id = id_
        self.city = city
        self.min_distance = min_distance
        self.position = position
        self.previous_min_dist_from_other_users = 10000.0
        self.is_active = True

    def __str__(self):
        text = "Vos information:"
        text += "\n ville: " + self.city
        text += "\n distance minimale: " + str(self.min_distance)
        text += "\n position: " + str(self.position)
        return text

    def get_id(self):
        return self.id

    def get_city(self):
        return self.city

    def get_position(self):
        return self.position

    def set_city(self, city):
        self.city = city

    def set_id(self, id_):
        self.id = id_

    def set_position(self, position):
        self.position = position

    def set_min_distance(self, dist):
        self.min_distance = dist

    def set_is_active(self, active):
        self.is_active = active

    def set_previous_min_distance_from_other_users(self, dist):
        self.previous_min_dist_from_other_users = dist

    def set_info(self, id_, city, min_distance, is_active):
        self.set_id(id_)
        self.set_city(city)
        self.set_min_distance(float(min_distance))
        self.set_is_active(is_active)
