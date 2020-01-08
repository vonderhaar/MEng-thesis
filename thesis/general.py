import statistics
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
import numpy as np
from classes import Course, Cohort, Semester, Student


def average(course):
	d = defaultdict(int)

	for sem_name in course.semester_names:
		sem = course.get(sem_name)
		total_registered = sem.get_num_registered() 
		print(sem_name)
		print('registered: ', total_registered)
		print('viewed: ', sem.get_num_viewed(), " ", sem.get_num_viewed()/total_registered, "%")
		print('explored: ', sem.get_num_explored(), " ", sem.get_num_explored()/total_registered, "%")
		print('completed: ', sem.get_num_completed(), " ", sem.get_num_completed()/total_registered, "%")
		print('verified: ', sem.get_average('verified'), "%")

		d['registered'] += total_registered
		d['viewed'] += sem.get_num_viewed()
		d['explored'] += sem.get_num_explored()
		d['completed'] += sem.get_num_completed()

	print('registered: ', d['registered'])
	print('viewed: ', d['viewed'], " ", d['viewed']/d['registered'], "%")
	print('explored: ', d['explored'], " ", d['explored']/d['registered'], "%")
	print('completed: ', d['completed'], " ", d['completed']/d['registered'], "%")

def grades(course):
	x, y = [], []
	counter = 0
	mod = 25 if course.is_1x else 5

	for entry in course.get_all_entries():

		if entry.completed and entry.grades != {}:
			counter += 1
			if counter % mod == 0:

				psets = entry.get_pset_average() if entry.get_pset_average() != None else 0
				quiz = entry.get_quiz() if entry.get_quiz() != None else 0
				final = entry.get_final() if entry.get_final() != None else 0

				if psets == 0 and quiz == 0 and final == 0:
					continue
				x.append(psets)
				y.append((quiz + final) / 2.0)

	print(counter)
	plt.clf()

	plt.scatter(x, y)
	plt.xlabel('Pset Average')
	plt.ylabel('Exam Average')
	plt.savefig("./grades" + '_' + course.ext, bbox_inches='tight')
	plt.clf()


def demo(course):
	age = [entry.age if (entry.age != None and entry.age > 7) else np.nan for entry in course.get_all_entries()]
	grades = [entry.get_grade() if (entry.completed and entry.get_grade() != None) else np.nan for entry in course.get_all_entries()]
	
	print('average age: ', np.nanmean(age), np.nanstd(age))
	print('% male: ', 1 - course.get_average('female'), " and female: ", course.get_average('female'))
	print('average grade if complete: ', np.nanmean(grades), np.nanstd(grades))
	print('average grade if complete: ', course.get_average('overall_grade', True))

def average_age_by_season(course):
	spring = Course()
	summer = Course()
	fall = Course()

	for sem in course.semester_names:
		semester = course.get(sem)
		if semester.season == 'spring':
			spring.add(sem, semester)
		elif semester.season == 'summer':
			summer.add(sem, semester)
		else:
			fall.add(sem, semester)

	spring_age = [entry.age if (entry.age != None and entry.age > 7) else np.nan for entry in spring.get_all_entries()]
	summer_age = [entry.age if (entry.age != None and entry.age > 7) else np.nan for entry in summer.get_all_entries()]
	fall_age = [entry.age if (entry.age != None and entry.age > 7) else np.nan for entry in fall.get_all_entries()]

	spring_percent = [1 if (entry.age != None and entry.age >= 12 and entry.age <= 19 and (entry.education_level == 'hs' or entry.education_level == 'jhs')) else 0 for entry in spring.get_all_entries()]
	summer_percent = [1 if (entry.age != None and entry.age >= 12 and entry.age <= 19 and (entry.education_level == 'hs' or entry.education_level == 'jhs')) else 0 for entry in summer.get_all_entries()]
	fall_percent = [1 if (entry.age != None and entry.age >= 12 and entry.age <= 19 and (entry.education_level == 'hs' or entry.education_level == 'jhs')) else 0 for entry in fall.get_all_entries()]

	print("spring age:", np.nanmean(spring_age), np.nanstd(spring_age))
	print("summer age:", np.nanmean(summer_age), np.nanstd(summer_age))
	print("fall age:", np.nanmean(fall_age), np.nanstd(fall_age))

	print("spring age:", np.mean(spring_percent))
	print("summer age:", np.mean(summer_percent))
	print("fall age:", np.mean(fall_percent))

def engagement_by_grade(course):
	cohorts = []
	for i in range(10):
		cohorts.append(Cohort())

	for entry in course.get_all_entries():
		grade = entry.get_grade()
		if grade == None or grade == 0:
			continue

		# take care of perfect scores
		if grade == 1.0:
			cohorts[9].add_entry(entry)
		else:
			cohorts[int(grade*10 % 10)].add_entry(entry)

	for i in range(len(cohorts)):
		print("cohort", i, ":", cohorts[i].get_average('overall_grade'))
		print(cohorts[i].get_average('active_days'), "active days")
		print(cohorts[i].get_average('problem_checks'), "problem checks")
		print(cohorts[i].get_average('videos'), "videos")
		print(cohorts[i].get_average('forum'), "forum")
		print(len(cohorts[i].dic.keys()))

	# write info to CSV for visualization
	filename = "./visualization/data/" + course.ext + "/engagement_by_grade.csv"
	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Bin","ActiveDays","ProblemChecks", "Videos", "Forum"])
		for i, cohort in zip(range(len(cohorts)), cohorts):
			grade_bin = str(i*10) + "-" + str(i*10+9 if i < 9 else 100)+"%"
			writer.writerow([grade_bin, cohort.get_average("active_days"), cohort.get_average('problem_checks'),
								cohort.get_average("videos"), cohort.get_average('forum')])

def start_time(course):
	copy = course.deep_copy()
	copy.delete(copy.self_paced_run)

	cohorts = defaultdict(Cohort)

	first = copy.get_semester_by_index(0)
	print((first.end_date - first.start_date).days)

	for entry in copy.get_all_entries():
		grade = entry.get_grade()
		if grade == None or grade == 0:
			continue

		days = (copy.get(entry.sem_name).start_date - entry.start_time).days
		cohorts[round(days)].add_entry(entry)

	sorted_keys = sorted(cohorts.keys(), reverse = True)
	x, y = [], []
	for key in sorted_keys:
		if key < -50:
			continue
		x.append(key)
		y.append(cohorts[key].get_average('completed'))

	plt.scatter(x, y, color="#184999")
	plt.xlabel('Number of days registered before start date')
	plt.ylabel('Completion rate')
	plt.yticks([0, 0.2, 0.4, 0.6])
	plt.savefig(str(course.is_1x) + "start_time", bbox_inches='tight')
	plt.clf()



def main(course_1x, course_2x):
	print("\n------------------------ GENERAL ----------------------\n")
	print('1x results:\n')
	start_time(course_1x)
	# average(course_1x)
	# grades(course_1x)
	# demo(course_1x)
	# average_age_by_season(course_1x)
	# engagement_by_grade(course_1x)

	print('\n2x results:\n')
	start_time(course_2x)
	# average(course_2x)
	# grades(course_2x)
	# demo(course_2x)
	# engagement_by_grade(course_2x)




