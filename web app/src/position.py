import googlemaps as gm

GM_API_KEY = "AIzaSyAcVPFRpZKPgnTv-29eDG1GLkOWEhpDhvw"
gm = gm.Client(key=GM_API_KEY)


class Position():
    """Class for managing users position"""
    def __init__(self, lat=48.866667, lng=2.333333):  # INIT POSITION A PARIS
        self.lat = lat
        self.lng = lng
        self.accuracy = 0.0

    def __str__(self):
        return f"Latitude: {self.lat}, longitude: {self.lng}"

    def gmDistance(self, lat_lng):
        """Return Google Map distance from a latitude and longitude."""
        res = gm.distance_matrix((self.lat, self.lng), (lat_lng))
        dist = self.convertStringToFloatAndMeter(res['rows']
                                                    [0]
                                                    ['elements']
                                                    [0]
                                                    ['distance']
                                                    ['text']
                                                 )
        return dist

    def convertStringToFloatAndMeter(self, val):
        """Convert the Google Maps distance to float."""
        unite_distance = val[-2:]
        if unite_distance == "km":
            coef_convertion = 1e3
        else:
            coef_convertion = 1
        if "m" in val:
            val = val.replace("m", "")
        if "k" in val:
            val = val.replace("k", "")
        if " " in val:
            val = val.replace(" ", "")
        return float(val)*coef_convertion

    def getCurrentPosition(self):
        """Use Google Maps to get the user current position."""
        coords = gm.geolocate()
        self.lat = coords['location']['lat']
        self.lng = coords['location']['lng']
        self.accuracy = coords['accuracy']
        return self
