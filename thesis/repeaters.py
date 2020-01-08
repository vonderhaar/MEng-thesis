import csv
import glob
import os
import statistics
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon
from classes import Course, Cohort, Semester, Student


# NOTE: this is usually called with data that has NOT removed never viewed people
def percentages_graph(viewed, explored, completed, image_name):
	plt.bar(range(1, len(viewed)+1), viewed, align='center', color='#c9e6f2')
	plt.bar(range(1, len(explored)+1), explored, align='center', color='#476ffa')
	plt.bar(range(1, len(completed)+1), completed, align='center', color='#03204f')

	plt.xlabel('total # of semesters registered')
	plt.ylabel("% of learners registered")
	plt.savefig(image_name, bbox_inches='tight')
	plt.clf()

	print('average completion new user: ', completed[0])
	print('average completion for repeated user: ', np.mean(completed[1:]))

def num_events_graph(days, ylabel, image_name):
	x = range(1, len(days) + 1)
	plt.bar(x, days, align='center', color='#476ffa')
	plt.xlabel('total # of semesters registered')
	plt.xticks(x, x)
	plt.ylabel("total number of active days")
	plt.savefig(image_name, bbox_inches='tight')
	plt.clf()

def aggregate(repeaters, ext):
	cohorts = []
	for i in range(17):
		cohorts.append(Cohort())

	for key in repeaters.get_keys():
		student = repeaters.get(key)
		cohorts[student.get_num_semesters()-1].add(student.userid, student)


	viewed = [np.mean([student.get_ever('viewed') for student in cohorts[i].dic.values()]) for i in range(len(cohorts))]
	explored = [np.mean([student.get_ever('explored') for student in cohorts[i].dic.values()]) for i in range(len(cohorts))]
	completed = [np.mean([student.get_ever('completed') for student in cohorts[i].dic.values()]) for i in range(len(cohorts))]
	num_days = [cohorts[i].get_average('active_days') for i in range(len(cohorts))]
	num_days = [days if days != None else 0 for days in num_days]

	print(len(cohorts[4].dic))
	percentages_graph(viewed, explored, completed, 'any_semester' + ext + '.png')
	num_events_graph(num_days, 'average number of days active', ext + 'days.png')

# REWRITE
def subsequent_repeaters(repeated_users, courses, image_name):
	ary = [0] * (len(courses)-1)
	num_complete = [0] * (len(courses)-1)
	num_explore1 = [0] * (len(courses)-1)
	num_explore2 = [0] * (len(courses)-1)
	two_time = 0
	everyone_else = 0
	already_complete = 0
	for student in repeated_users:
		if len(repeated_users[student]) == 2:
			if repeated_users[student][0]['completed']:
				already_complete += 1
				# print(repeated_users[student][0]['certified'], repeated_users[student][1]['completed'])
				continue;
			two_time += 1
			time1, time2 = repeated_users[student][0]['semester'], repeated_users[student][1]['semester']
			index1, index2 = courses.index(time1), courses.index(time2)
			ary[index2-index1-1] += 1
			num_complete[index2-index1-1] += 1 if repeated_users[student][1]['completed'] else 0
			num_explore1[index2-index1-1] += 1 if repeated_users[student][0]['explored'] else 0
			num_explore2[index2-index1-1] += 1 if repeated_users[student][1]['explored'] else 0
		elif len(repeated_users[student]) > 2:
			everyone_else += 1
	print("total number subsequent: ", ary[0] / sum(ary))
	print("total number skipped exactly 1 semester: ", ary[1] / sum(ary))
	print("total number not subsequent: ", sum(ary[2:])/sum(ary))

	plt.bar(range(0, len(ary)), ary, align='center')
	plt.xlabel('# of semesters between runs')
	plt.ylabel('# of learners')
	# plt.savefig(image_name, bbox_inches='tight')
	plt.clf()

	plt.bar(range(0, len(ary)), [complete/total for complete, total in zip(num_complete, ary)], align='center')
	plt.xlabel('# of semesters between runs')
	plt.ylabel('percent learners who completed')
	# plt.savefig("a_"+image_name, bbox_inches='tight')
	plt.clf()

	explore1 = statistics.mean([x/total - y/total for x,y,total in zip(num_explore2, num_explore1, ary)])
	# explore2 = statistics.mean(num_explore2) / statistics.mean(ary)
	print("percent_increase between semesters:  ", explore1)
	
	print("already_complete ", already_complete / (already_complete + everyone_else+two_time))
	print("two_time ", two_time)
	print("everyone_else ", everyone_else)
	print("percent: ", two_time/(already_complete + everyone_else+two_time))
	# ax = plt.subplot(1,1,1)
	# ax.bar(x-0.2, [x/total for x, total in zip(num_explore1[:6], ary[:6])], align='center', width=0.4, color="0.75")
	# ax.bar(x+0.2, [x/total for x, total in zip(num_explore2[:6], ary[:6])], align='center', width=0.4, color="blue")
	# plt.xlabel('# of semesters between runs')
	# plt.ylabel('difference in exploration')
	# plt.savefig("b_"+image_name, bbox_inches='tight')
	# plt.clf()

def main(course1x, course2x, repeaters_1x, repeaters_2x):
	print("\n------------------------ REPEATERS ----------------------\n")
	print('1x results:\n')
	aggregate(repeaters_1x, '1x')

	print('2x results:\n')
	aggregate(repeaters_2x, '2x')
