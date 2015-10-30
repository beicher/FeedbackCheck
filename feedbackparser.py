import csv
# the following attempts to guess at the format of strings and
# make them into dates, which is handy because it looks like
# peerfeedback occasionally does the date format differently
# (not sure so far why)
from dateutil.parser import parse
# a specialized type of dictionary that makes it easier to
# combine dictionaries after each round of operation
# from collections import Counter

hw0_deadline = parse("2015-09-02 08:00:00")
hw0_tasks = 3
hw1_deadline = parse("2015-09-09 08:00:00")
hw1_tasks = 5
hw2_deadline = parse("2015-10-01 08:00:00")
hw2_tasks = 3
hw3_deadline = parse("2015-10-14 08:00:00")
hw3_tasks = 2



def give_credit(filename, deadline, tasks):
    # dictionary will be a set of keys (student addresses) paired with
    # simple integer values tracking how many assignments a given student
    # completed prior to the dealine
    completed = {}
    with open(filename, 'rb') as csvfile:
        gradereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in gradereader:
            # skip the heading row
            if row[0] != "Grader":
                # add student if it's someone we haven't seen
                if not completed.has_key(row[0]):
                    completed[row[0]] = 0
                # Date parsed by Python into a datetime object
                submit_date = parse(row[3])
                #print "Student: " + row[0]
                # this renders the gap between deadline and submit time
                # in the form of seconds, and then adds on the seconds the
                # system registered that it took before someone submitted
                timegap = (deadline - submit_date).total_seconds() + int(row[4])
                #print timegap
                if timegap < 0:
                    #print "Late submit: " + str(submit_date)
                    pass
                else:
                    #print "OK submit: " + str(submit_date)
                    completed[row[0]] += 1
    # update dictionary values to reflec how many points someone earned
    # 1.5 = full credit (all assigned tasks done by deadline)
    # 0 = no credit
    for student in completed.keys():
        if completed[student] < tasks:
            completed[student] = 0
        else:
            completed[student] = 1.5

    return completed

def update_gradefile(scores_dict):
    with open("gradebook-before.csv", 'rb') as csvfile:
        with open('gradebook-rulechange.csv', 'wb') as csvfile2:
            gradereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            gradewriter = csv.writer(csvfile2, delimiter=',', quotechar='|')
            for row in gradereader:
                if row[0] == "Student ID":
                    row.append("New Peer Feedback (HW Extra Credit) [0.01]")
                    gradewriter.writerow(row)
                else:
                    this_student = row[0] + "@gatech.edu"
                    if scores_dict.has_key(this_student):
                        #row[-1] = scores_dict[this_student]
                        row.append(scores_dict[this_student])
                    gradewriter.writerow(row)


def report_data(scores_dict):
    # render contents of a dictionary into a form where
    # it's easy to print out a summary
    total_students = len(scores_dict.keys())
    print "Found " + str(total_students) + " students."
    total_awarded = sum(scores_dict.values())
    print "Total of " + str(total_awarded) + " points awarded."
    late_students = scores_dict.values().count(0)
    scored_students = total_students - late_students
    if scored_students == 0:
        avg_score = 0
    else:
        avg_score = total_awarded / (scored_students * 1.0)
    print str(late_students) + " students received no credit."
    print "Remainder averaged " + str(avg_score)

def merge_values(overall, new):
    # take the new data for a specific assignment, and merge it into
    # the overall data
    for key in new.keys():
        if not key in overall.keys():
            overall[key] = new[key]
        else:
            overall[key] += new[key]

    return overall

def main():
    student_scores = {}
    hw_scores = give_credit("HW0NoComments.csv", hw0_deadline, hw0_tasks)
    print "HW0: "
    report_data(hw_scores)
    merge_values(student_scores, hw_scores)

    hw_scores = give_credit("HW1NoComments.csv", hw1_deadline, hw1_tasks)
    print "\nHW1: "
    report_data(hw_scores)
    merge_values(student_scores, hw_scores)

    hw_scores = give_credit("HW2NoComments.csv", hw2_deadline, hw2_tasks)
    print "\nHW2: "
    report_data(hw_scores)
    merge_values(student_scores, hw_scores)

    hw_scores = give_credit("HW3NoComments.csv", hw3_deadline, hw3_tasks)
    print "\nHW3: "
    report_data(hw_scores)
    merge_values(student_scores, hw_scores)

    print "\nAll Combined: "
    report_data(student_scores)

    update_gradefile(student_scores)


if __name__ == "__main__":
    main()
