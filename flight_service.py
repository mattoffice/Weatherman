import http.client
import weather_service


class Flight_Service:
    def __init__(self, city):
        self.city = city

    def call_flight_api(self):
        conn = http.client.HTTPSConnection(
            "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            'x-rapidapi-key': "306b476548msha99785a02beece4p105c70jsn7936c1aeaca3"
        }

        conn.request(
            "GET", "/apiservices/autosuggest/v1.0/UK/GBP/en-GB/?query={0}".format(self.city), headers=headers)

        res = conn.getresponse()
        data = res.read()

        decoded = data.decode("utf-8")
        return decoded
