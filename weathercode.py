
import geocoder
from pyowm import OWM

def weather_tag():
    g = geocoder.ip('me')
    lat, lng = g.latlng

    owm = OWM('8aa4f173bbbb157abbce710e59499f7c')  # Replace YOUR_API_KEY with your OpenWeatherMap API key
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat, lng)
    weather = observation.weather

    print(f"Current weather: {weather.detailed_status}")
    w = weather.detailed_status

    w_final = ""

    if w == "clear sky":
        w_final = "CS"
    elif w == "few clouds" or w == "scattered clouds" or w == "broken clouds" or w == "overcast clouds":
        w_final = "C"
    elif w == "shower rain" or w == "rain" or w == "thunderstorm":
        w_final = "R"
    elif w == "snow":
        w_final = "S"
    else:
        w_final = "M"

    return w_final

