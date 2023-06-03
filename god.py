import person
from person import *
#from proliferation import *

import random

# path
path_human_book_prefix = current_file_dir + "/profiles/humanbook" # the first generation
path_death_book = current_file_dir + "/profiles/death_book.csv"
path_history_book_prefix = current_file_dir + "/profiles/historybook"


# global parameters
num_first_generation = 200
num_personal_qualities = 5
magic_ratio = 0.2

# society parameters
person_container = []
start_date = datetime.date(1, 1, 1)
end_date = datetime.date(50, 12, 30)

# handle history
acient_container = []
max_buffer_acients = 10

# record holder
records = {"credit": None, "longevity": None}


def midwife(person_id, fam_id):
    # innate qualities: intelligence boldness specificity generalization
    qualities = [random.randint(1, 100) for i in range(0, num_personal_qualities)]
    return Person(person_id, random.randint(0, 1), 1, fam_id, qualities)


def human_genesis():
    # human_book: generation zero
    output_file = open(path_human_book_prefix + '_generation_0.csv', 'w')

    # creat the generation zero
    for i in range(0, num_first_generation):
        # creat human
        new_born = midwife(i, i)
        person_container.append(new_born)

        # output content to the file
        output_file.write(new_born.output_with_formats(","))

    # new_born.get_header()
    output_file.close()


def examiner(candidates):
    for i in candidates:
        # check credits
        if records["credit"]:
            if i.credits >= records["credit"].credits:
                records["credit"] = i
        else:
            records["credit"] = i

        # check longevity
        if records["longevity"]:
            if i.get_longevity() >= records["longevity"].get_longevity():
                records["longevity"] = i
        else:
            records["longevity"] = i


def death_reporter(individual, book_path):
    # add the past to history book
    acient_container.append(individual)

    # release buffer and uopdate the records
    if len(acient_container) == max_buffer_acients:
        # update the records
        examiner(acient_container)

        # output
        history_book = open(book_path, "w")
        for thepast in acient_container:
            history_book.write(thepast.output_with_formats(","))

        # refresh container
        acient_container.clear()
        history_book.close()

def history_writer(book_path):
    # TODO output alive

    # TODO output dead

    # output records
    history_book = open(book_path, "w")
    for i in story_teller():
        history_book.write(i + "\n")

def story_teller():
    lines = []

    if len(acient_container) != 0:
        lines.append(",".join(acient_container[0].get_output_header))

        if records["credit"]:
            lines.append(records["credit"].output_with_formats(","))
        else:
            lines.append("None")

        if records["longevity"]:
            lines.append(records["longevity"].output_with_formats(","))
        else:
            lines.append("None")
        return lines
    else:
        return ["Nothing"]


def mourner(date):
    for individual in person_container:
        if (death_id, date) in individual.events:
            individual.alive = False

            # output to the history_book
            death_reporter(individual)

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
        id_ev_happening = random.randint(1, len(events_df))

        # life-saver (if event is death)
        if id_ev_happening == death_id:
            if decision_maker.should_be_saved():
                continue

        # get age at the day
        age_by_today = decision_maker.get_age(current_date)

        # add to life events (sanity check for event will be executed in the following func)
        decision_maker.insert_lifebook(id_ev_happening, 1, age_by_today, "afterbirth_passive")
        decision_maker.events = apply_time_rules(decision_maker.events)


def philanthropist():
    # pick a portion of human to explore intelligence
    charity_event = random.sample(person_container, int(len(person_container) * magic_ratio))
    for philanthropist in charity_event:
        # donate 10% money
        philanthropist.credits *= 0.9

        # gain 10% fortune (TODO: gain reputation)
        philanthropist.fortune *= 1.1


def employer():
    # pick a portion of employer to change a job
    company = random.sample(person_container, int(len(person_container) * magic_ratio))
    for employer in company:
        if employer.job.title is not None:
            # exam by intelligenceL=: (employer.intelligence -70 + 100)/100
            employer.job.salary *= (employer.intelligence + 30)/100

def payer():
    # get current worker
    employers = [person for person in person_container if person.job.title is not None]

    # pay each person who has a job
    for employer in employers:
        employer.credits += employer.job.salary


def a_normal_day(current_date):
    # TODO

    # work
    employer()

    # match-making
    match_maker(current_date)

    # intellectual growth
    lecturer()

    # charity
    philanthropist()

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

        # pay once a year
        if current_date.year > 1:
            if current_date.month == 1 and current_date.day == 1:
                payer()

                # write history every 3 years
                if current_date.year % 3 == 0:
                    history_writer(book_path=path_history_book_prefix + current_date.strftime('_%Y-%m-%d.csv'))




human_genesis()
time_machine()
print(story_teller())
