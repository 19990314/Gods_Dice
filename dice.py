import random
import os
import pandas as pd

# current path
current_file_dir = os.path.dirname(os.path.abspath(__file__))

# table: life events
events_df = pd.read_csv(current_file_dir + '/hidden_variables/events.csv')
events_df = events_df.set_index(events_df.columns[0])
min_destinity_events = 0
max_destinity_events = 4

# get a random number with normal distribution by given the max and min range, mean, and standard deviation
def random_in_normal_distribution(lower, upper, mean, std):
    while True:
        if mean == 0 and std ==0:
            # NOT in_normal_distribution
            return random.randint(lower, upper)
        else:
            # in_normal_distribution
            num = random.normalvariate(mean, std)
            if lower <= num <= upper:
                return num


def random_samples(list, ratio):
    portion_size = int(len(list) * ratio)  # Select 20% of the list
    return random.sample(list, portion_size)


# return a list of events for destiny (with event id and age of happening)
def destiny_dice():
    des_events = []

    # random events
    num_destiny_ev = random_in_normal_distribution(min_destinity_events, max_destinity_events, 3, 1)
    indices_destiny_ev = random.sample(range(len(events_df)), int(num_destiny_ev))

    # for each event
    for event_id in indices_destiny_ev:
        event = events_df.iloc[event_id]
        age_happening = random_in_normal_distribution(event["age_min"], event["age_max"], event["age_mean"],
                                                      event["age_std"])
        # [id, dest_flag, age]
        des_events.append([event_id, int(age_happening)])

    # sort by age
    des_events = sorted(des_events, key=lambda x: x[1])
    return des_events


# correct the events in unnatural order
def apply_time_rules(events):
    new_events = {}

    # eliminate everything after death
    for i in events.keys():
        if events_df.iloc[i[0]-1]["event"] == "death":
            break
        else:
            new_events[i] = events[i]

    return new_events


def event_is_reasonable(event_id, age):
    happen_flag = True

    # Not happening: the age is out of the range
    if events_df.iloc[event_id - 1]["control"] == 1:
        # Rule: age difference > age std
        if abs(age - events_df.iloc[event_id - 1]["age_mean"]) > events_df.iloc[event_id - 1]["age_std"] * 2:
            happen_flag = False

    return happen_flag