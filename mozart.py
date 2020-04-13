from amadeus import Client, ResponseError, Location


def main():

    api_key = 'Z9Fb2VEMHPrPue68nDfMhPV5Z8cj1YT3'
    api_secret = 'cRtDOOmAuRKL9RUv'

    amadeus = Client(
        client_id=api_key,
        client_secret=api_secret
    )

    res1 = amadeus.reference_data.locations.get(
        keyword='Bang',
        subType=Location.ANY
    )
    dest = res1.data[0]['iataCode']
    print(dest)

    try:
        print(test)
        print(dest)
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode='LGW',
            destinationLocationCode=str(dest),
            departureDate='2020-07-01',
            adults=1)
        print(response.data)
    except ResponseError as error:
        print(error)


if __name__ == '__main__':
    main()

# 'https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=PAR&maxPrice=200' -H 'Authorization: Bearer HABOkvssqbsvSiSAND3IWA0xUjtU'
