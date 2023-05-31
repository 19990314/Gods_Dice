import datetime
import ephem
import random
import pandas as pd
import os
from thedice import *

magic_ratio = 0.2

# table: jobs profile
jobs_profile = pd.read_csv(current_file_dir + '/hidden_variables/jobs_vs_salaries.csv')

# dictionary: zodiac information
zodiac_profile = pd.read_csv(current_file_dir + '/hidden_variables/zodiac_profiles.csv')
zodiac_map = {}
for index, row in zodiac_profile.iterrows():
    zodiac_map[row['Zodiac_Sign']] = row['Zodiac_ID']

# setup standard global values
intelligence_standard = 50
boldness_standard = 50

# jobs
annual_income_increase_rate = 0.1
salary_deviation = 0.1
zodiac_deviation = 0.1

# special events
death_id = 5
marriage_id = 2

# basic information about a person instance
header_person_profile = None

# marriage wait list
singles = []


class Person:
    def __init__(self, person_id, gender, year, family_id, qualities, dad=None, mom=None):
        # basic info
        self.person_id = person_id
        self.gender = gender
        self.birth_year, self.birth_month, self.birth_day = self.generate_birthday(year)
        self.alive = True
        self.gender = gender
        self.credits = 0
        self.job = Job()

        # innate qualities: intelligence boldness specificity generalization
        self.intelligence = qualities[0]
        self.fortune = qualities[1]
        self.boldness = qualities[2]
        self.generalization = qualities[3]
        self.specificity = qualities[4]

        # family
        self.family_id = family_id
        self.inherit(dad, mom)
        self.partner = None
        self.child = []

        # zodiac sign
        self.constellation = self.find_constellation()

        # event records: use (event_id, Date) as key, mapping to two variables:
        # 1: a flag (destiny or not)
        # 2: age (when would it happen)
        self.init_destinies()

    def get_zodiac_id(self, constellation):
        return

    def init_destinies(self):
        self.events = {}

        # god's dice: 30% destiny
        des_events = destiny_dice()
        for i in des_events:
            self.insert_lifebook(i[0], i[1], i[2], "prenatal")

        # sanity check the events
        self.events = apply_time_rules(self.events)

    def insert_lifebook(self, event_id, destiny_flag, age, assigner_imprint):
        # prenatal timeline
        if age < 0:
            return

        # event = marriage, then go for a date
        if event_id == marriage_id:
            singles.append(self)
            return

        happen_flag = 1

        # Not happening: the age is out of the range
        if events_df.iloc[event_id]["control"] == 1:
            if abs(age - events_df.iloc[event_id]["age_mean"]) > events_df.iloc[event_id]["age_std"]:
                happen_flag = 0

        if happen_flag == 1:
            # add event to lifebook
            event_date = self.get_birthday_daytime() + datetime.timedelta(days=int(age * 365))
            self.events[(event_id, event_date)] = [destiny_flag, age, assigner_imprint]

            # sort the lifebook by age
            self.events = dict(sorted(self.events.items(), key=lambda x: x[0][1]))

    def generate_birthday(self, year):

        # define the start and end date of the year
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)

        # select a random date
        time_between_dates = end_date - start_date
        random_number_of_days = random.randint(0, time_between_dates.days)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        return random_date.year, random_date.month, random_date.day

    def inherit(self, dad, mom):
        # initial credit
        if dad is None and mom is None:
            credit_pool = 3000
            self.credits = credit_pool * self.fortune / 100

        else:
            # inherit credits from parents
            credit_pool = magic_ratio * (dad.credits + mom.credits)
            self.credits = credit_pool * self.fortune / 100

            # qualities: family balance
            self.intelligence = (self.intelligence + dad.intelligence + mom.intelligence) / 3
            self.boldness = (self.boldness + dad.boldness + mom.boldness) / 3
            self.generalization = (self.generalization + dad.generalization + mom.generalization) / 3
            self.specificity = (self.specificity + dad.specificity + mom.specificity) / 3

    def get_birthday_daytime(self):
        return datetime.date(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self, today):
        age_by_today = today - self.get_birthday_daytime()
        return age_by_today.days / 365

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

        return constellation[1]

    def constellationalize(self, family_id):
        return

    def dating_happily(self, theother, date):
        feedback = 100

        # age gap: for every 3 years, cut 10%
        gap = int((self.get_age(date) - theother.get_age(date)) / 3)
        feedback *= (1 - 0.1 * gap)

        # TODO: other factors

        if feedback > 60:
            return True
        else:
            return False

    def marry(self, partner):
        self.partner = partner
        partner.partner = self

    def get_output_header(self):
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
                    profile.append(str(self.job.title))
                    profile.append(str(self.job.salary))
                elif attr == 'partner':
                    if self.partner is None:
                        profile.append("None")
                    else:
                        profile.append(str(self.partner.person_id))
                else:
                    profile.append(str(getattr(self, attr, None)))

        return deliminator.join(profile) + "\n"


class Job:
    def __init__(self):
        self.title = None
        self.salary = None

    def get_job(self):
        # randomly get a job
        random_job = jobs_profile.sample(n=1).values[0]

        # extract job info
        self.title = random_job[1]
        self.salary = random_job[2] * (1 + salary_deviation * random.randint(-3, 3))

    def update_salary(self, work_age, intelligence, boldness):
        self.salary *= (100 + boldness - intelligence_standard) / 100
        self.salary *= (100 + intelligence - boldness_standard) / 100
        self.salary *= 1 + (work_age * annual_income_increase_rate)
