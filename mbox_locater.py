from mapbox import Geocoder

geocoder = Geocoder(
    access_token="pk.eyJ1IjoibWF0dG9mZmljZSIsImEiOiJjazlqdHYwZ2kwMHBxM2xscmF5bzdpc2dsIn0.iDUw71WZCer5ZrbOkEusqg")

response = geocoder.forward("13 Algernon Terrace North Shields")

print(response.status_code)
print(response.json()['features'][0]['geometry']['coordinates'])
