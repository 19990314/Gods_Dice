class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.get_weather()


    def get_weather(self):
        import pyowm

        # Create an instance of the OWM API wrapper
        owm = pyowm.OWM('your-API-key')

        # Specify the latitude and longitude
        lat = 51.5074
        lon = -0.1278

        # Search for the weather at the specified location
        observation = owm.weather_at_coords(lat, lon)
        weather = observation.get_weather()

        # Get the temperature, wind speed, and weather status
        temperature = weather.get_temperature('celsius')['temp']
        wind_speed = weather.get_wind()['speed']
        status = weather.get_status()

        # Print the results
        print(f"Temperature: {temperature}°C")
        print(f"Wind speed: {wind_speed} m/s")
        print(f"Weather: {status}")

        return 0
