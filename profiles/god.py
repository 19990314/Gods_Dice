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


def time_pusher():

    current_date = start_date

    # execute the model day by day
    while current_date <= end_date:

        # pick 30% person to take actions

        #

        # next day
        current_date += datetime.timedelta(days=1)



human_genesis()
