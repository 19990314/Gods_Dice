import person
from person import *
from proliferation import *

import random

# global parameters
num_first_generation = 1000
num_personal_qualities = 4
path_human_book = "./humanbook"

# society parameters
person_container = []
start_date = datetime.date(1, 1, 1)
end_date = datetime.date(500, 12, 30)
death_id = 5

def give_birth(person_id, fam_id):
    # innate qualities: intelligence boldness specificity generalization
    qualities = [random.randint(1, 100) for i in range(0,num_personal_qualities)]
    return Person(person_id, random.randint(0, 1), 1, fam_id, qualities)


def human_genesis():
    # human_book: generation zero
    output_file = open(path_human_book + '_generation_0.csv', 'w')

    # creat the generation zero
    for i in range(0, num_first_generation):
        # creat human
        new_born = give_birth(i, i)
        person_container.append(new_born)

        # output content to the file
        output_file.write(new_born.output_with_formats(","))

    new_born.get_header()
    output_file.close()

def mourner(date):
    for individual in person_container:
        if (death_id, date) in individual.events:
            # remove the record
            person_container.remove(individual)

            # TODO output to the history_book


def event_messenger(affecting_ratio):
    # 30% chance to take actions
    person_indices = random.sample(range(len(person_container)), int(affecting_ratio * len(person_container)))

    # take actions
    for i in person_indices:
        decision_maker = person_container[i]
        # TODO

def a_normal_day():
    # TODO

def time_machine():

    current_date = start_date

    # execute the model day by day
    while current_date <= end_date:
        # check lives
        mourner(current_date)

        # choose 30% people to take actions
        event_messenger(0.3)

        # refresh everyone
        a_normal_day()

        # next day
        current_date += datetime.timedelta(days=1)



human_genesis()
time_machine()