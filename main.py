import csv
import json
import itertools


student_division_json = open(file='./input/student_division.json', mode='r')
student_division_data = json.load(student_division_json)
student_division_json.close()


def get_grade_array(grades):
    grade_array = []

    grade_range_array = grades.split()
    if grade_range_array[2] != 'currentYear':
        from_grade = int(grade_range_array[0])
        to_grade = int(grade_range_array[2])
        for grade in range(from_grade, to_grade + 1):
            grade_array.append(grade)
    else:
        grade_array.append(int(grade_range_array[0]))

    return grade_array


def get_all_array_proper_subsets(array):
    array_proper_subsets = []
    for i in range(1, len(array)+1):
        subsets_of_length_i = itertools.combinations(array, i)
        for subset in subsets_of_length_i:
            array_proper_subsets.append(subset)
    return array_proper_subsets


for board in student_division_data:
    for grades in student_division_data[board]:
        subject_array = student_division_data[board][grades]
        subject_array_combinations = get_all_array_proper_subsets(
            subject_array)
        grade_array = get_grade_array(grades)

        for grade in grade_array:

            for subjects in subject_array_combinations:
                periods = []
                for subject in subjects:
                    period = '{} {} {}'.format(board, grade, subject)
                    periods.append(period)

                periods_no_space = []
                for period in periods:
                    periods_no_space.append(period.replace(" ", ""))

                subjects_str = ' '.join(subjects).replace(' ', '_')
                file_name = './output/' + \
                    "{}_{}_{}".format(
                        board, grade, subjects_str) + '.csv'
                # with open(file_name, mode='w') as file_to_write:
                rows_to_write = []
                with open(file='./input/timetable.csv', mode='r') as file_to_read:
                    reader = csv.reader(file_to_read)
                    new_rows = []
                    for row in reader:
                        if row[0] == 'DAY/TIME':
                            new_rows.append(row)
                            continue
                        new_row = []
                        new_row.append(row[0])
                        for i in range(1, len(row)):

                            # print(row[i], periods)
                            # print(row[i].replace(" ", "") in periods_no_space)
                            if row[i].replace(" ", "") in periods_no_space:
                                new_row.append(row[i])
                            else:
                                new_row.append('-')
                        new_rows.append(new_row)
                    with open(file_name, mode='w') as file_to_write:
                        file_writer = csv.writer(file_to_write)
                        file_writer.writerows(new_rows)
