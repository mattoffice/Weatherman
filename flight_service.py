import http.client
import weather_service
from amadeus import Client, ResponseError, Location


class Flight_Service:
    def __init__(self, city, date):
        self.city = city
        self.outbound_date = date
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
                subType=Location.CITY
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
                    departureDate=self.outbound_date,
                    adults=1)
                if(len(response.data) == 0):
                    print(
                        'No flights could be found for this location on this date.  Try a different location and/or date!')
                else:
                    for res in response.data:
                        print("Flight: Departing {departure_location} at {departure_time}.  Price: {price}".format(departure_location=str(res['itineraries'][0]['segments']
                                                                                                                                          [0]['departure']['iataCode']), departure_time=str(res['itineraries'][0]['segments']
                                                                                                                                                                                            [0]['departure']['at']), price=str(res['price']['total'])))
                        """
                        print(res['price']['total'])
                        print(res['itineraries'][0]['segments']
                              [0]['departure']['iataCode'])
                        print(res['itineraries'][0]['segments']
                              [0]['departure']['at'])
                        """
                        # txt1 = "Flight: {f}, I'am {age}".format(fname = "John", age = 36)
            except ResponseError as error:
                print(error)
