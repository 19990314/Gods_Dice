import random
import os
import pandas as pd

# Get the current directory
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


# return a list of events for destiny (with event id and age of happening)
def destiny_dice():
    des_events = []
    num_destiny_ev = random_in_normal_distribution(min_destinity_events, max_destinity_events, 3, 1)
    indices_destiny_ev = random.sample(range(len(events_df)), int(num_destiny_ev))
    for event_id in indices_destiny_ev:
        event = events_df.iloc[event_id]
        age_happening = random_in_normal_distribution(event["age_min"], event["age_max"], event["age_mean"],
                                                      event["age_std"])

        des_events.append([event_id, 1, age_happening])
    return des_events


# correct the events in unnatural order
def apply_time_rules(events):
    new_events = {}

    return new_events