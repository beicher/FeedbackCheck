import csv
# the following attempts to guess at the format of strings and
# make them into dates, which is handy because it looks like
# peerfeedback occasionally does the date format differently
# (not sure so far why)
from dateutil.parser import parse
# a specialized type of dictionary that makes it easier to
# combine dictionaries after each round of operation
from collections import Counter

hw0_deadline = parse("2015-09-02 08:05:00")
hw0_per = 0.5
hw1_deadline = parse("2015-09-09 08:05:00")
hw1_per = 0.3
hw2_deadline = parse("2015-10-01 08:05:00")
hw2_per = 0.5
hw3_deadline = parse("2015-10-14 08:05:00")
hw3_per = 0.75



def give_credit(filename, deadline, per_task):
    hw_scores = Counter({})
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != "Grader":
                if not hw_scores.has_key(row[0]):
                    hw_scores[row[0]] = 0
                submit_date = parse(row[3])
                #print "Student: " + row[0]
                if submit_date > deadline:
                    #print "Late submit: " + str(submit_date)
                    pass
                else:
                    #print "OK submit: " + str(submit_date)
                    hw_scores[row[0]] += per_task

    return hw_scores

def update_gradefile(scores_dict):
    with open("gradebook-before.csv", 'rb') as csvfile:
        with open('gradebook-after.csv', 'wb') as csvfile2:
            gradereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            gradewriter = csv.writer(csvfile2, delimiter=',', quotechar='|')
            for row in gradereader:
                if row[0] == "Student ID":
                    row.append("New Peer Feedback (HW Extra Credit) [0.01]")
                    gradewriter.writerow(row)
                else:
                    this_student = row[0] + "@gatech.edu"
                    if scores_dict.has_key(this_student):
                        row.append(scores_dict[this_student])
                    gradewriter.writerow(row)


def report_data(scores_dict):
    total_students = len(scores_dict.keys())
    print "Found " + str(total_students) + " students."
    total_awarded = sum(scores_dict.values())
    print "Total of " + str(total_awarded) + " points awarded."
    late_students = scores_dict.values().count(0)
    scored_students = total_students - late_students
    avg_score = total_awarded / (scored_students * 1.0) 
    print str(late_students) + " students received no credit."
    print "Remainder averaged " + str(avg_score)
    
def main():
    student_scores = Counter({})
    hw_scores = give_credit("HW0NoComments.csv", hw0_deadline, hw0_per)
    print "HW0: "
    report_data(hw_scores)
    student_scores += hw_scores
    
    hw_scores = give_credit("HW1NoComments.csv", hw1_deadline, hw1_per)
    print "\nHW1: "
    report_data(hw_scores)
    student_scores += hw_scores

    hw_scores = give_credit("HW2NoComments.csv", hw2_deadline, hw2_per)
    print "\nHW2: "
    report_data(hw_scores)
    student_scores += hw_scores

    hw_scores = give_credit("HW3NoComments.csv", hw3_deadline, hw3_per)
    print "\nHW3: "
    report_data(hw_scores)
    student_scores += hw_scores
    
    print "\nAll Combined: "
    report_data(student_scores)

    update_gradefile(student_scores)


if __name__ == "__main__":
    main()
