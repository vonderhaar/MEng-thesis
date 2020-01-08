import copy
import csv
import pandas as pd
from collections import defaultdict
from classes import Course, Cohort, Semester, Student


# ctas_1x = Group()
# ctas_2x = Group()

# def get_ctas():
# 	return (ctas_1x, ctas_2x)

# def get_uninteractive():
# 	return uninteractive_dict

# def get_cheaters():
# 	return cheaters_dict

def remove_instructors(course):
	instructors = set()
	ctas = defaultdict(list)

	for sem_name in course.semester_names:
		file_add = sem_name[:2]
		xls = pd.ExcelFile('/Volumes/Research/admin_data/staff_ctas_600'+file_add+'.xlsx')
		sheet = pd.read_excel(xls, sem_name[3:], header=None)
		num = 0
		for name in sheet[0]:
			if pd.isna(name):
				break;
			instructors.add(name)
		for name in sheet[5]:
			if pd.isna(name):
				break
			ctas[name].append(sem_name)

	for sem_name in course.get_keys():
		semester = course.get(sem_name)
		sem_copy = semester.deep_copy()
		for userid in semester.get_keys():
			entry = semester.get(userid)
			if entry.username in ctas.keys():
				cta = copy.deepcopy(entry)
				cta.is_cta = semester.name in ctas[entry.username]
				# ctas_1x.add_entry(cta) if course.is_1x else ctas_2x.add_entry(cta)
				if semester in ctas[entry.username]:
					semester.delete(userid)
			if entry.username in instructors:
				sem_copy.delete(userid)
		course.add(sem_copy.name, sem_copy) # automatically overwrites old one

def remove_never_viewed(course):
	for sem_name in course.get_keys():
		semester = course.get(sem_name)
		sem_copy = semester.deep_copy()
		for userid in semester.get_keys():
			if not semester.get(userid).viewed:
				sem_copy.delete(userid)
		course.add(sem_copy.name, sem_copy) # automatically overwrites old one

def get_all_cheaters(course):
	cheaters = defaultdict(list)
	for i in range(len(course.semester_names)-1, -1, -1):
		sem_i = course.get_semester_by_index(i)
		for userid in sem_i.get_keys():
			student = sem_i.get(userid)
			counter = 0
			for j in range(0, i):
				sem_j = course.get_semester_by_index(j)
				if student.userid in sem_j.get_keys():
					last_event = sem_j.get(student.userid).last_event
					if last_event != None and last_event > sem_i.start_date and last_event < sem_i.end_date:
						counter += 1
			if counter >= 2:
				cheaters[sem_i.name].append(userid)
	return cheaters

def remove_cheaters_and_uninteractive(course):
	updated_map = {} 
	cheater_counter = 0
	uninteractive_counter = 0
	overlap_counter = 0 

	cheaters = get_all_cheaters(course)

	for sem_name in course.get_keys():
		semester = course.get(sem_name)
		sem_copy = semester.deep_copy()
		for userid in semester.dic:
			entry = semester.get(userid)
			if entry.explored and entry.num_forum_events in (0, None) and entry.num_videos in (0, None) and entry.num_problem_checks in (0, None):
				uninteractive_counter += 1
				# uninteractive_dict[key].append(result[key])
				sem_copy.delete(entry.userid)
			if entry.userid in cheaters[semester.name]:
				cheater_counter += 1
				if entry.userid not in sem_copy.get_keys():
					overlap_counter += 1
					continue
				# cheaters_dict[key].append(result[key])
				sem_copy.delete(entry.userid)
		course.add(sem_copy.name, sem_copy) # automatically overwrites old one

	print ('accessed within current course', cheater_counter - overlap_counter)
	print ('uninteractive within course', uninteractive_counter - overlap_counter)
	print ('accessed within AND uninteractive within course', overlap_counter)


def clean(course_raw, verbose = False):
	# print(type(course_raw))
	course = course_raw.deep_copy()
	remove_instructors(course)
	remove_never_viewed(course)
	remove_cheaters_and_uninteractive(course)
	return course
