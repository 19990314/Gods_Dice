from god import *

class TimeMahine:
    def __init__(self):
        self.start_time = None
        self.start_date = datetime.date(1, 1, 1)
        self.end_date = datetime.date(100, 12, 30)

    def start(self):
        self.start_time = time.time()

        # generation 1
        human_genesis()

        # start time machine
        print("Time machine started.")
        current_date = self.start_date

        # execute the model day by day
        while current_date <= self.end_date:
            # refresh the day
            a_normal_day(current_date, self.start_time)

            # next day
            current_date += datetime.timedelta(days=1)



# program starts here
digit_world = TimeMahine()
digit_world.start()