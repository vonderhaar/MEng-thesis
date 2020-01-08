import csv
import copy
import sys
from collections import defaultdict
import datetime
from classes import Course, Cohort, Semester, Student, Entry
import traceback



# returns (userid, Entity) tuple
def make_entry(row, sem_name, start_date):
	userid = row[1]
	username = row[2]
	viewed = True if row[4] == 'true' else False
	explored = True if row[5] == 'true' else False
	certified = True if row[6] == 'true' else False
	completed = True if row[7] == 'true' else False
	education_level = None if row[22] == '' else row[22]
	age = None if row[23] == '' else (start_date - datetime.datetime(int(row[23]), 7, 2)).days/365 # July 2nd is the middlemost day of the year
	gender = None if row[24] == '' else row[24]
	grade = 0 if row[25] == '' else float(row[25])
	start_time = None if row[27] == '' else datetime.datetime.strptime(row[27][:19], '%Y-%m-%d %H:%M:%S')
	first_event = None if row[28] == '' else datetime.datetime.strptime(row[28][:19], '%Y-%m-%d %H:%M:%S')
	last_event = None if row[29] == '' else datetime.datetime.strptime(row[29][:19], '%Y-%m-%d %H:%M:%S')
	num_events = None if row[30] == '' else int(row[30])
	num_active_days = None if row[31] == '' else int(row[31])
	num_forum_events = None if row[43] == '' else int(row[43])
	num_videos = None if row[61] == '' else int(row[61])
	num_problem_checks = None if row[41] == '' else int(row[41])
	mode = None if row[44] == '' else row[44]
	return (userid, Entry(sem_name, userid, username, viewed, explored, certified, completed, education_level, 
				age, gender, grade, start_time, first_event, last_event, num_events,
				num_active_days, num_forum_events, num_videos, num_problem_checks, mode))

def load_dictionaries(course):
	dates_map = make_course_run_dates(course)
	counter = 0
	for sem_name in course.semester_names:
		semester = Semester(sem_name, course.is_1x, sem_name == course.self_paced_run, dates_map[sem_name])
		with open('/Volumes/Research/person_course_data/6.00.' + sem_name + '_person_course.csv') as csv_file:
			data = csv.reader(csv_file, delimiter=',')
			for row in data:
				if row[0] != 'course_id': # skip header row
					entry = make_entry(row, sem_name, dates_map[sem_name][0])
					semester.add(entry[0], entry[1])
		try:
			with open('/Volumes/Research/grade_report_data/6.00.' + sem_name + '_grade_report.csv') as csv_file:
				data = csv.reader(csv_file, delimiter=',')
				keys = None
				for row in data:
					if row[1] == 'Email': # skip header row
						index_of_first = -1
						index_of_final = -1
						for i, cell in enumerate(row):
							if 'Grade' in cell:
								index_of_first = i
							if 'Final' in cell:
								index_of_final = i
						keys = row[index_of_first : index_of_final+1]
					else:							
						grades = {}
						for i in range(len(keys)):
							grades[keys[i]] = None if row[i+3] == "Not Attempted" else float(row[i+3])
						entry = semester.get(row[0])
						if entry != None and grades != {}:
							entry.set_grades(grades)

		except Exception:
			print(sem_name)
			traceback.print_exc()


		course.add(sem_name, semester)



def make_repeaters(course):
	repeaters = Cohort()
	for entry in course.get_all_entries():
		repeaters.add_entry(entry)
	return repeaters

def make_course_run_dates(course):
	dates_map = {}
	file = 'runs_6001x.txt' if course.is_1x else 'runs_6002x.txt'
	index = 0
	is1x = file == 'runs_6001x.txt'

	print(course.semester_names)
	with open('/Volumes/Research/admin_data/'+file) as f:
		lines = f.readlines()
		for i in range(0, len(lines), 4):
			start_date = datetime.datetime.strptime(lines[i+1][:-5], 'Course Start Date: %b %d, %Y %H:%M')
			end_date = datetime.datetime.strptime(lines[i+2][:-5], 'Course End Date: %b %d, %Y %H:%M')
			# get season
			semester = course.semester_names[index]
			season = "spring"
			if '3T' in semester or ('2T' in semester and (semester[-2:] == "_2" or semester[-1] == "a")):
				season = "fall"
			elif '2T' in semester:
				season = "summer"
			dates_map[semester] = [start_date, end_date, season]
			index += 1
	return dates_map


