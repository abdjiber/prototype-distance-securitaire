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

    def getId(self):
        return self.id

    def getCity(self):
        return self.city

    def getPosition(self):
        return self.position

    def setCity(self, city):
        self.city = city

    def setId(self, id_):
        self.id = id_

    def setPosition(self, position):
        self.position = position

    def setMinDistance(self, dist):
        self.min_distance = dist

    def setIsActive(self, active):
        self.is_active = active

    def setPreviousMinDistanceFromOtherUsers(self, dist):
        self.previous_min_dist_from_other_users = dist

    def setInfo(self, id_, city, min_distance, is_active):
        self.setId(id_)
        self.setCity(city)
        self.setMinDistance(float(min_distance))
        self.setIsActive(is_active)
