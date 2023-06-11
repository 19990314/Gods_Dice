import person
from person import *
# from proliferation import *
import time
import random

# path
path_human_book_prefix = current_file_dir + "/profiles/humanbook"  # the first generation
path_death_book = current_file_dir + "/profiles/death_book.csv"
path_history_book_prefix = current_file_dir + "/profiles/historybook"

# global parameters
num_first_generation = 1000
num_personal_qualities = 5
magic_ratio = 0.2

# society parameters
person_container = []

# handle history
acient_container = []
max_buffer_acients = 50

# record holder
records = {"credit": None, "longevity": None}
classroom = []


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


def record_breaker(candidates):
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


def death_reporter(individual):
    # add the past to history book
    acient_container.append(individual)

    # release buffer and uopdate the records
    if len(acient_container) == max_buffer_acients:
        # update the records
        record_breaker(acient_container)

        # output to history_book
        history_book = open(path_death_book, "w")
        for thepast in acient_container:
            history_book.write(thepast.output_with_formats(","))

        # refresh acient_container -> empty
        for i in acient_container:
            acient_container.remove(i)
        history_book.close()


def historian(journal_path):
    # TODO output alive

    # TODO output dead

    # output records
    journal = open(journal_path, "w")

    # statistics about the dead people
    for i in story_teller():
        journal.write(i)

    # close file
    journal.close()


def story_teller():
    # lines: header, the richest one, the oldest one
    lines = []

    # TODO
    if records["credit"]:
        # header
        try:
            lines.append(",".join(acient_container[0].get_output_header()) + "\n")
        except IndexError:
            print("header issue")

        # the richest one
        lines.append(f"The richest one: #{records['credit'].person_id} holds ${records['credit'].credits}")
        lines.append(records["credit"].output_with_formats(","))

        # the oldest one
        lines.append(f"The richest one: #{records['longevity'].person_id} holds ${records['longevity'].credits}")
        lines.append(records["longevity"].output_with_formats(","))
        return lines
    else:
        return ["Nothing"]


def mourner(individual, age, assigner_imprint):
    # alive flag becomes longevity
    individual.alive = age

    # edit lifebook
    individual.insert_lifebook(death_id, 1, age, assigner_imprint= assigner_imprint)

    # output to the history_book
    death_reporter(individual)

    # remove the record
    try:
        person_container.remove(individual)
    except ValueError:
        print("individual")


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


def lecturer(current_date):
    for student in classroom:
        # grow 10%
        student.intelligence *= 1 + 0.1

        # get age at the day
        age_by_today = student.get_age(current_date)

        # add to life events (sanity check for event will be executed in the following func)
        student.insert_lifebook(education_id, 1, age_by_today, "afterbirth_passive")
        # student.events = apply_time_rules(student.events)


def event_messenger(current_date):
    # finish todos
    if current_date in todo_events.keys():
        for destiny_pair in todo_events[current_date]:
            # apply
            event_practician(who=destiny_pair[0], what=destiny_pair[1], when=current_date, assigner_imprint="prenatal")

    # take actions: a portion of people
    for decision_maker in random_samples(person_container, magic_ratio):
        # rolling dice for an event
        id_ev_happening = random.randint(1, len(events_df))
        while id_ev_happening == 12:  # birthday
            id_ev_happening = random.randint(1, len(events_df))
        # apply
        event_practician(who=decision_maker, what=id_ev_happening, when=current_date,
                         assigner_imprint="afterbirth_passive")


def event_practician(who, what, when, assigner_imprint):
    # get age at the day
    age_by_today = who.get_age(when)

    if event_is_reasonable(what, age_by_today):
        # life-saver (if event is death)
        if what == death_id:
            # live or not
            if who.should_be_saved():
                return
            else:
                # mark the death
                mourner(individual=who, age=age_by_today, assigner_imprint = assigner_imprint)
        else:
            # add to life events (sanity check for event will be executed in the following func)
            who.insert_lifebook(what, 1, age_by_today, assigner_imprint=assigner_imprint)
            # decision_maker.events = apply_time_rules(decision_maker.events)


def philanthropist(current_date):
    # pick a portion of human to explore intelligence
    charity_event = random.sample(person_container, int(len(person_container) * magic_ratio))
    for philanthropist in charity_event:
        # donate 10% money
        philanthropist.credits *= 0.9

        # gain 10% fortune (TODO: gain reputation)
        philanthropist.fortune *= 1.1

        # get age at the day
        age_by_today = philanthropist.get_age(current_date)

        # add to life events (sanity check for event will be executed in the following func)
        philanthropist.insert_lifebook(education_id, 1, age_by_today, "afterbirth_passive")
        # philanthropist.events = apply_time_rules(philanthropist.events)


def employer(current_date):
    # pick a portion of person as candidates
    company = random_samples(employee, magic_ratio)

    # promote or demote -> update salary
    for candidate in company:
        # get age at the day
        age_by_today = candidate.get_age(current_date)

        # exam work "capability"
        candidate.job.update_salary(age_by_today, candidate.capacity_at_work())


def payer():
    # pay each person who has a job
    for employer in employee:
        employer.credits += employer.job.salary


def a_normal_day(current_date, start_time):
    # TODO

    # choose 30% people to take actions
    event_messenger(current_date)

    # match-making: data & marry
    match_maker(current_date)

    # intellectual growth
    lecturer(current_date)

    # philanthropist: do charity
    philanthropist(current_date)

    # employee: promote/demote
    employer(current_date)

    # every Jan.1
    if current_date.year > 1:

        if current_date.month == 1 and current_date.day == 1:
            # employer: pay
            payer()

            # check: to-do list

            # write history every 3 years
            if current_date.year % 3 == 0:
                # output records
                historian(journal_path=path_history_book_prefix + current_date.strftime('_%Y-%m-%d.csv'))

                # report time used
                time_uesed = time.time() - start_time
                print(f"By {current_date.year}: {time_uesed:.2f} seconds.")
