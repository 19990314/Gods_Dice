from person import *
import random

# global parameters
num_first_generation = 1000
num_qualities = 4
path_human_book = "./human_book"


def give_birth(person_id, fam_id):
    # innate qualities: intelligence boldness specificity generalization
    qualities = [random.randint(1, 100) for i in range(0,num_qualities)]
    return Person(person_id, random.randint(0, 1), 1, fam_id, qualities)


def human_genesis():
    # human_book: generation zero
    output_file = open(path_human_book + '_0.csv', 'w')

    # creat the generation zero
    for i in range(0, num_first_generation):
        # creat human
        new_born = give_birth(i, i)

        # output content to the file
        output_file.write(new_born.output_with_formats(","))

    output_file.close()



human_genesis()