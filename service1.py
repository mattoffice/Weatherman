import requests
import simplejson as json


def main():
    """
    value = input(
        "Which planet do you want to know about? Type a number between 1 and 10 - or however many planets there are...!\n")
    """

    response = requests.get(
        "https://swapi.co/api/planets/")

    print(response.status_code)

    print(response.json())

    jayson = response.json()

    string = response.text

    #planets = json.loads(string)

    for key in jayson:
        if (key == 'results'):
            #print("JSN.RESULTS IS TYPE: " + str(type(jayson[key])))
            for i in range(len(jayson[key])):
                print("PLANET: " + str(i) + ": " + str(jayson[key][i]['name']))
                i += 1

            #print(key, '--->', jayson[key])

    # for planet in planets:
    #   print("The planet is called: " + planet.results['name'])


if __name__ == '__main__':
    main()
