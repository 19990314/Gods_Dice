import datetime
import ephem
import random


class Person:
    def __init__(self, person_id, gender, year, family_id, qualities):
        self.person_id = person_id
        self.gender = gender
        self.birth_year, self.birth_month, self.birth_day = self.generate_birthday(year)
        self.family_id = family_id
        self.inherit(family_id)

        # innate qualities: intelligence boldness specificity generalization
        self.intelligence = qualities[0]
        self.boldness = qualities[1]
        self.specificity = qualities[2]
        self.generalization = qualities[3]

        self.job = Job()

        # zodiac sign
        self.constellation = self.find_constellation()

    def generate_birthday(self, year):

        # define the start and end date of the year
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        # select a random date
        time_between_dates = end_date - start_date
        random_number_of_days = random.randint(0, time_between_dates.days)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date.year, random_date.month, random_date.day


    def inherit(self, family_id):
        return

    def get_birthday_daytime(self):
        return datetime.datetime(self.birth_year, self.birth_month, self.birth_day)

    def find_constellation(self):
        # Convert the date object to a string
        date_str = self.get_birthday_daytime().strftime('%Y/%m/%d')

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

    def output_with_formats(self, deliminator):
        return deliminator.join([str(getattr(self, attr, None)) for attr in self.__dict__ if not callable(getattr(self, attr))]) + "\n"


class Job:
    def __init__(self, title_id, salary):
        self.title = title_id
        self.salary = salary