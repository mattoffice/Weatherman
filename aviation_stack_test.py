import requests


def main():

    params = {
        'access_key': '3972ff343d74f61f20cce4d1616d705f',
        'arr_iata': 'AIY'
    }

    api_result = requests.get(
        'http://api.aviationstack.com/v1/routes', params)

    api_response = api_result.json()
    print(api_response)

    for flight in api_response['data']:
        print(flight)
        if (flight['city_name'] == 'London'):
            print(u'%s IATA code.' % (
                flight['iata_code']))


if __name__ == '__main__':
    main()
