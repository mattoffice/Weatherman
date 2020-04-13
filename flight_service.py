import http.client
import weather_service
from amadeus import Client, ResponseError, Location


class Flight_Service:
    def __init__(self, city):
        self.city = city
        self.api_key = 'Z9Fb2VEMHPrPue68nDfMhPV5Z8cj1YT3'
        self.api_secret = 'cRtDOOmAuRKL9RUv'

    def call_amadeus(self):

        amadeus = Client(
            client_id=self.api_key,
            client_secret=self.api_secret
        )

        try:
            amadeus_resp = amadeus.reference_data.locations.get(
                keyword=str(self.city),
                subType=Location.ANY
            )
            if(amadeus_resp.data):
                desired_location = amadeus_resp.data[0]['iataCode']
                print("Destination: " + str(desired_location))
            else:
                print('This location could not be found by amadeus flight search')
        except ResponseError as error:
            print(str(error.code))

        if(amadeus_resp.data):
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode='LGW',
                    destinationLocationCode=str(desired_location),
                    departureDate='2020-07-01',
                    adults=1)
                if(len(response.data) == 0):
                    print(
                        'No flights could be found for this location on this date.  Try a different location and/or date!')
                else:
                    for res in response.data:
                        print(res['price'])
            except ResponseError as error:
                print(error)
