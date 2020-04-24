from amadeus import Client

api_key = 'Z9Fb2VEMHPrPue68nDfMhPV5Z8cj1YT3'
secret = 'cRtDOOmAuRKL9RUv'

amadeus = Client(
    client_id=api_key,
    client_secret=secret
)

resp = amadeus.shopping.flight_destinations.get(
    origin='LON',  departureDate='2020-04-17')

for r in resp.data:
    print("**************************************************************")
    print("There is a cheap flight from {0}, to {1}, departing on {2}".format(
        r['origin'], r['destination'], r['departureDate']))
