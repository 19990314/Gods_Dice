import datetime
import ephem


class Person:
    def __init__(self, name, gender, year, month, day, family_id):
        self.name = name
        self.gender = gender
        self.birthday = datetime.date(year, month, day)
        self.family_id = family_id
        self.inherit(family_id)

        self.constellation = self.find_constellation()

    def inherit(self, family_id):
        return

    def find_constellation(self):
        # Convert the date object to a string
        date_str = self.birthday.strftime('%Y/%m/%d')

        # Create an observer object at the Greenwich Observatory
        observer = ephem.Observer()
        observer.lat = '51.4772'
        observer.lon = '-0.0005'

        # Set the observer date to the specified date
        observer.date = date_str

        # Calculate the constellation of the sun
        sun = ephem.Sun()
        sun.compute(observer)
        constellation = ephem.constellation(sun)

        # Print the result
        print(f"The constellation on {date_str} is {constellation[1]}")

        return constellation[1]

    def constellationalize(self, family_id):
        return