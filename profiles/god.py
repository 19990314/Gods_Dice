import person
from person import *
from proliferation import *

import random

# path
path_human_book = "./humanbook"
path_history_book = "./history_book.csv"

# global parameters
num_first_generation = 1000
num_personal_qualities = 5
magic_ratio = 0.2

# society parameters
person_container = []
start_date = datetime.date(1, 1, 1)
end_date = datetime.date(5, 12, 30)

# handle history
acient_container = []
max_buffer_acients = 200


def midwife(person_id, fam_id):
    # innate qualities: intelligence boldness specificity generalization
    qualities = [random.randint(1, 100) for i in range(0, num_personal_qualities)]
    return Person(person_id, random.randint(0, 1), 1, fam_id, qualities)


def human_genesis():
    # human_book: generation zero
    output_file = open(path_human_book + '_generation_0.csv', 'w')

    # creat the generation zero
    for i in range(0, num_first_generation):
        # creat human
        new_born = midwife(i, i)
        person_container.append(new_born)

        # output content to the file
        output_file.write(new_born.output_with_formats(","))

    #new_born.get_header()
    output_file.close()


def history_writer(individual):
    # add the past to history book
    acient_container.append(individual)

    # release buffer
    if len(acient_container) == max_buffer_acients:
        # output
        history_book = open(path_history_book, "w")
        for thepast in acient_container:
            history_book.write(thepast.output_with_formats(","))

        # refresh container
        acient_container.clear()
        history_book.close()


def mourner(date):
    for individual in person_container:
        if (death_id, date) in individual.events:
            individual.alive = False

            # output to the history_book
            history_writer(individual)

            # remove the record
            person_container.remove(individual)


def match_maker(current_date):
    while len(singles) > 0:
        partner_one = singles.pop(0)

        # random selection
        if len(singles) > 0:
            partner_two = random.choice(singles)
            singles.remove(partner_two)

            # check compatibility
            if partner_one.dating_happily(partner_two, current_date):
                # then marry or not
                partner_one.marry(partner_two)


def lecturer():
    # pick a portion of human to explore intelligence
    course = random.sample(person_container, int(len(person_container) * magic_ratio))
    for student in course:
        # grow 10%
        student.intelligence *= 1 + 0.1


def event_messenger(current_date):
    # 30% chance to take actions
    person_indices = random.sample(range(len(person_container)), int(magic_ratio * len(person_container)))

    # take actions
    for i in person_indices:
        decision_maker = person_container[i]

        # rolling dice for an event
        id_ev_happening = random.randint(0, len(events_df) - 1)

        # check age
        age_by_today = decision_maker.get_age(current_date)

        # add to life events (sanity check for event will be executed in the following func)
        decision_maker.insert_lifebook(id_ev_happening, 1, age_by_today, "afterbirth_passive")
        decision_maker.events = apply_time_rules(decision_maker.events)


def a_normal_day(current_date):
    # TODO

    # match-making
    match_maker(current_date)

    # intellectual growth
    lecturer()

    # check lives
    mourner(current_date)


def time_machine():
    current_date = start_date

    # execute the model day by day
    while current_date <= end_date:

        # choose 30% people to take actions
        event_messenger(current_date)

        # refresh everyone
        a_normal_day(current_date)

        # next day
        current_date += datetime.timedelta(days=1)

        a = person_container


human_genesis()
time_machine()
