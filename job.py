import pandas as pd
import os
import random
from hidden_variables.personality_var import *

# current path
current_file_dir = os.path.dirname(os.path.abspath(__file__))

# table: jobs profile
jobs_profile = pd.read_csv(current_file_dir + '/hidden_variables/jobs_vs_salaries.csv')

# job variables
annual_income_increase_rate = 0.1
salary_deviation = 0.1
salary_mean = 60000

class Job:
    def __init__(self):
        self.title = None
        self.salary = None
        # career history:{title: [[age, salary],[age, salary],...]
        self.career_history = {}

    def get_job(self, age, capacity_list):
        # randomly get a job
        random_job = jobs_profile.sample(n=1).values[0]

        # test capability
        job_salary = random_job[2] * (1 + salary_deviation * random.randint(-3, 3))
        if age > 15 and self.pass_interview(candidate_age=age,candidate_capacity=capacity_list, job_salary=job_salary):
            # extract job info
            self.title = random_job[1]
            self.salary = job_salary

            # save history:{title: [[age, salary],[age, salary],...]
            if self.title not in self.career_history.keys():
                self.career_history[self.title] = []
            self.career_history[self.title].append([age, self.salary])
            return True
        else:
            return False

    def pass_interview(self, candidate_age, candidate_capacity, job_salary):
        # one year away from 40: cut 3 points
        score = 100
        score -= abs(40 - candidate_age) * 3

        # capacity: TODO
        score += candidate_capacity

        # work age
        if self.career_history.keys():
            work_age = self.work_age(title=list(self.career_history.keys())[0], current_age=candidate_age)
            score += work_age * 3

        if job_salary/salary_mean < score/100:
            return True
        else:
            return False

    def work_age(self, title, current_age):
        if title in self.career_history.keys():
            work_years = current_age - self.career_history[self.title][0][0]
            return work_years

    def update_salary(self, current_age, candidate_capacity):
        self.salary *= (100 + candidate_capacity - 50) / 100
        work_age = self.work_age(title = list(self.career_history.keys())[-1], current_age = current_age)
        self.salary *= 1 + (work_age * annual_income_increase_rate)