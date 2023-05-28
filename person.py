import datetime
import ephem
import random
import pandas as pd
import os

# Get the current directory
current_file_dir = os.path.dirname(os.path.abspath(__file__))

# read jobs profile
jobs_profile = pd.read_csv(current_file_dir + '/hidden_variables/jobs_vs_salaries.csv')

# zodiac informations
zodiac_profile = pd.read_csv(current_file_dir + '/hidden_variables/zodiac_profiles.csv')
zodiac_map = {}
for index, row in zodiac_profile.iterrows():
    zodiac_map[row['Zodiac_Sign']] = row['Zodiac_ID']

# setup standard values
intelligence_standard = 50
boldness_standard = 50
annual_income_increase_rate = 0.1
salary_deviation = 0.1
zodiac_deviation = 0.1

# basic information about a person instance
header_person_profile = []



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

        # zodiac sign
        self.constellation = self.find_constellation()

        # event records
        self.destiny = {}
        self.events = {}

    def get_zodiac_id(self, constellation):
        return

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

    def get_header(self):
        for attr in self.__dict__:
            if not callable(getattr(self, attr)):
                if attr == 'job':
                    header_person_profile.append("job.salary")
                    header_person_profile.append("job.salary")
                else:
                    header_person_profile.append(attr)



    def output_with_formats(self, deliminator):
        profile = []
        for attr in self.__dict__:
            if not callable(getattr(self, attr)):
                if attr == 'job':
                    this_job = getattr(self, attr, None)
                    profile.append(this_job.title)
                    profile.append(this_job.salary)
                else:
                    profile.append(str(getattr(self, attr, None)))

        return deliminator.join(profile) + "\n"


class Job:
    def __init__(self):
        random_job = jobs_profile.sample(n=1).values[0]
        print("A")
        self.title = random_job[1]
        self.salary = random_job[2] * (1 + salary_deviation * random.randint(-3, 3))



    def update_salary(self, work_age, intelligence, boldness):
        self.salary *= (100 + boldness - intelligence_standard)/100
        self.salary *= (100 + intelligence - boldness_standard)/100
        self.salary *= 1 + (work_age*annual_income_increase_rate)