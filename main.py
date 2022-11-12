from datetime import datetime
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
import requests

LATITUDE = 12.971599
LONGITUDE = 77.594566

try:
    my_latitude = float(input("Enter your latitude: "))
except ValueError:
    my_latitude = LATITUDE
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise

try:
    my_longitude = float(input("Enter your latitude: "))
except ValueError:
    my_longitude = LONGITUDE
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise

print(f"{my_latitude = }")
print(f"{my_longitude = }")

parameters = {
    "lat": my_latitude,
    "lng": my_longitude,
    "formatted": 0,
    }

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()


def local_time(date_time, local_time_zone):

    date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S%z")
    date_time = date_time.replace(tzinfo=timezone('UTC'))
    updated_local_time = date_time.astimezone(tz=timezone(local_time_zone))
    return updated_local_time


def time_zone(lat, lng):
    tf = TimezoneFinder()
    tz_local = tf.certain_timezone_at(lat=lat, lng=lng)
    print(f"Your time zone: {tz_local}")
    return tz_local


time_zone_local = time_zone(lat=my_latitude, lng=my_longitude)
sunrise = local_time(data["results"]["sunrise"], time_zone_local)
sunset = local_time(data["results"]["sunset"], time_zone_local)

print(f"Today Sunrise for your location will be at {sunrise.hour}H:{sunrise.minute}m:{sunrise.second}s")
print(f"Today Sunset for your location will be at {sunset.hour}H:{sunset.minute}m:{sunset.second}s")



