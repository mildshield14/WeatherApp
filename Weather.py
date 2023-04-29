import json

from google.auth.transport import requests
import requests
import spacy


class Weather:
    def __init__(self, phrase):
        self.phrase = phrase
        self.nlp = spacy.load("en_core_web_sm")

    # code from: https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python/

    def get_location(self, city=None):
        if city is None:
            ip_address = requests.get('https://api.ipify.org').text
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        else:
            response = requests.get(f'https://ipapi.co/{city}/json/').json()

        location_data = {
            "ip": response.get("ip"),
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        return location_data

    def get_ip(self):
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]

    def get_city(self, city):
        with open("files/world-cities_json.json") as f:
            data = json.load(f)
            city=city.title()
            if city in [city["name"] for city in data]:
                return True
            return False

    def weather(self):

        doc = self.phrase
        city = self.get_city(doc)

        if not city:
            # City not found in the input phrase
            city = self.get_location()['city']
        else:
            city = doc.title()
        api_key = "a218965593f1fc41a36edc67a53e99c7"

        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # complete_url variable to store
        # complete url address
        complete_url = base_url + "appid=" + api_key + "&q=" + city

        # get method of requests module
        # return response object
        response = requests.get(complete_url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
        if x["cod"] != "404":
            # store the value of "main"
            # key in variable y
            y = x["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"]

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidity = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]

            print(str(current_temperature) + " is the temperature in " + city)
            print(str(current_pressure) + " is the pressure in " + city)
            print(str(current_humidity) + " is the humidity in " + city)
            print(str(weather_description) + " is the weather description " + city)

            return_for_email = (str(current_temperature) + " is the temperature in " + city + "\n" + str(
                current_pressure) + " is the pressure in " + city + "\n" \
                                + str(current_humidity) + " is the humidity in " + city + "\n" + str(
                        weather_description) + " is the weather description " + city)

            return return_for_email

weatherObj = Weather("Montreal")
message = weatherObj.weather()
print(message)