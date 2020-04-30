import time
import requests


def call_weather_api():

    response = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast?q=Madrid&appid=23b9b2cda2de73f546fb9ac14d881d73")

    tomorrow_date = time.gmtime(
        response.json()['list'][0]['dt']).tm_mday + 1

    print(tomorrow_date)
    time_obj = time.gmtime(response.json()['list'][0]['dt'])
    print(time_obj.tm_mon)

    if time_obj.tm_mon == 4 or 6 or 9 or 11 and time_obj.tm_mday == 30:
        tomorrow_date = 1
    elif time_obj.tm_mday == 31:
        tomorrow_date = 1

    print(tomorrow_date)

    data = get_results_for_tomorrow(response, tomorrow_date)
    return data


def get_results_for_tomorrow(response, tomorrow_date):
    # print(tomorrow_date)
    results = []
    for forecast in response.json()['list']:
        text = forecast['dt_txt']
        sub_s = text[8:10]
        if (sub_s == str(tomorrow_date)):
            # print(text)
            results.append(forecast)
        return results

    #print("*****************************\nTime in 24 hrs: \n")
    #print(datetime.now() + timedelta(days=1))
    # print(response.json()['list'][0])

    #tomorrow_date = time.gmtime(response.json()['list'][0]['dt']).tm_mday + 1


twenty_four_hours = 86400

response = call_weather_api()
