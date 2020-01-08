import csv
import glob
import os
import copy
import statistics
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from classes import Course, Cohort, Semester, Student


def self_vs_instructor(course):
	self_paced_results = defaultdict(list)
	course_instructor = course.deep_copy()
	sem_self = course.get(course.self_paced_run)
	course_instructor.delete(course.self_paced_run)
	
	print('AVERAGE OF INSTRUCTOR-LED RUNS:')
	print('completion % overall: ', course_instructor.get_completion_rate())
	print('average grade overall: ', course_instructor.get_average('overall', True))
	print('average grade overall: ', course_instructor.get_average('overall_1', True))
	# print('average active days overall: ', course_instructor.get_average('active_days'))
	# print('average active days overall (completed): ', course_instructor.get_average('active_days', True))
	# print('average final (completed): ', course_instructor.get_average('final', True))
	# print('average quiz (completed): ', course_instructor.get_average('quiz', True))
	# print('average psets (completed): ', course_instructor.get_average('pset', True))
	# print('average finger (completed): ', course_instructor.get_average('finger_exercises', True))

	print()
	print('SELF PACED RUN:')
	print('completion % overall: ', sem_self.get_completion_rate())
	print('average grade overall: ', sem_self.get_average('overall', True))
	print('average grade overall: ', sem_self.get_average('overall_1', True))
	# print('average active days overall: ', sem_self.get_average('active_days'))
	# print('average active days overall (completed): ', sem_self.get_average('active_days', True))
	# print('average final (completed): ', sem_self.get_average('final', True))
	# print('average quiz (completed): ', sem_self.get_average('quiz', True))
	# print('average psets (completed): ', sem_self.get_average('pset', True))
	# print('average finger (completed): ', sem_self.get_average('finger_exercises', True))



def self_vs_instructor_repeater(repeaters, course):
	self_paced_run = course.self_paced_run
	index_of_self_paced = course.semester_names.index(self_paced_run)
	test_in = Cohort()
	test_out = Cohort()
	test = Cohort()
	control = Cohort()

	retook_dic = defaultdict(list)

	for userid in repeaters.get_keys():
		student = repeaters.get(userid)
		if repeaters.get_num_semesters(userid) >= 2:
			if student.is_in_semester(self_paced_run):
				# add to test_in
				entity = student.get(self_paced_run)
				new_student = Student(student.userid)
				new_student.add(self_paced_run, entity)
				test_in.add(userid, new_student)
				# add to test_out
				new_student = student.deep_copy()
				# print(new_student.get_keys())
				test.add(userid, new_student)
				new_student.delete(self_paced_run)
				test_out.add(userid, new_student)
			else:
				control.add(userid, student.deep_copy())

			for sem_name in student.get_keys():
				if course.is_first_or_last_semester(sem_name):
					continue
				retook_dic[sem_name].append(0 if sem_name == student.get_last_semester(course.semester_names) else 1)


	print()
	print('REPEATERS WHO DIDNT TAKE SELF-PACED:')
	print('completion % overall: ', control.get_completion_rate())
	print('average grade overall: ', control.get_average('overall', True))
	print('average grade overall: ', control.get_average('overall_1', True))
	print('ever completed:', control.get_ever_completed_rate())

	print()
	print('REPEATERS IN SELF-PACED DURING SELF-PACED SEM:')
	print('completion % overall: ', test_in.get_completion_rate())
	print('average grade overall: ', test_in.get_average('overall', True))
	print('average grade overall: ', test_in.get_average('overall_1', True))
	print('ever completed:', test_in.get_ever_completed_rate())

	print()
	print('REPEATERS IN SELF-PACED DURING INSTRUCTOR-LED SEM:')
	print('completion % overall: ', test_out.get_completion_rate())
	print('average grade overall: ', test_out.get_average('overall', True))
	print('average grade overall: ', test_out.get_average('overall_1', True))
	print('ever completed:', test_out.get_ever_completed_rate())

	print()
	print('RETAKING COURSE')
	ls = []
	for key in retook_dic:
		if key == self_paced_run:
			print("self paced", statistics.mean(retook_dic[key]))
		else:
			ls.append(statistics.mean(retook_dic[key]))
	print("instructor ", statistics.mean(ls))

	x = [0, 1, 2, 4, 5]
	x_labels = ['ever', 'self\n\n\nGroup A', 'instuctor', 'ever', '\n\n\nGroup B', 'instuctor']
	y = [test.get_ever_completed_rate(), test_in.get_completion_rate(), test_out.get_completion_rate(), control.get_ever_completed_rate(), control.get_completion_rate()]
	plt.bar(x, y, align='center')
	plt.ylabel('% of learners who complete', fontsize=12)
	plt.xticks([0, 1, 2, 4, 4.5, 5], x_labels, fontsize = 12)
	plt.savefig("anything" + ("1x" if course.is_1x else "2x")+ ".png", bbox_inches='tight')
	plt.clf()


def main(course_1x, course_2x, repeaters_1x, repeaters_2x):
	print("\n------------------------ PACE ----------------------\n")
	# print('1x results:')
	self_vs_instructor(course_1x)	

	# self_vs_instructor_repeater(repeaters_1x, course_1x)
	# print('\n\n2x results:')
	self_vs_instructor(course_2x)
	# self_vs_instructor_repeater(repeaters_2x, course_2x)






