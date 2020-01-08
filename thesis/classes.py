from collections import defaultdict
import statistics
import copy

class BigGroup(object):

	def __init__(self):
		self.dic = {}

	def add(self, key, value):
		self.dic[key] = value

	def delete(self, key):
		del self.dic[key]

	def get(self, key):
		if key not in self.dic.keys():
			return None
		return self.dic[key]

	def get_keys(self):
		return self.dic.keys()

	def get_completion_rate(self):
		return sum([item.get_completion_rate() for item in self.dic.values()]) / len(self.dic)

	def get_award_rate(self):
		return sum([item.get_award_rate() for item in self.dic.values()]) / len(self.dic)

	def get_average(self, stat, complete = False, overall = True):
		ls = []

		if overall:
			for entry in self.get_all_entries():
				if (complete and entry.completed) or not complete:
					value = entry.get_stat(stat)
					if value != None:
						ls.append(value)
		else:
			for item in self.dic.values():
				value = item.get_average(stat, complete)
				if value !=  None:
					ls.append(value)
		if len(ls) == 0:
			return None
		return sum(ls) / len(ls)

	def get_all_entries(self):
		ls = []
		for item in self.dic.values():
			ls.extend(item.get_all_entries())
		return ls

	def get_all_userids(self):
		userids = set()
		for item in self.dic.values():
			userids.update(item.get_keys())
		return userids

# a collection of Semester objects
class Course(BigGroup):

	def __init__(self, semester_names = None, self_paced_run = None, is_1x = True, promo_dict = {}):
		super().__init__()
		self.semester_names = semester_names
		self.self_paced_run = self_paced_run
		self.is_1x = is_1x
		self.promo_dict = promo_dict
		self.ext = '1x' if self.is_1x else '2x'

	def __str__(self):
		return "Course 1x" if self.is_1x else "Course 2x"

	def delete(self, key):
		del self.dic[key]
		self.semester_names.remove(key)

	def get_semester_by_index(self, index):
		return self.dic[self.semester_names[index]]

	def get_index_by_semester(self, semester_name):
		return self.semester_names.index(semester_name)

	def is_first_or_last_semester(self, semester_name):
		return self.get_index_by_semester(semester_name) == 0 or self.get_index_by_semester(semester_name) == len(self.semester_names)-1

	def get_num_registered(self):
		return sum([sem.get_num_registered() for sem in self.dic.values()])

	def deep_copy(self):
		new_course = Course(self.semester_names[:], self.self_paced_run, self.is_1x, self.promo_dict)
		for sem in self.dic.values():
			new_course.add(sem.name, sem.deep_copy())
		return new_course

# a collection of Student objects
class Cohort(BigGroup):
	def __init__(self):
		super().__init__()

	def add_entry(self, entry):
		if entry.userid not in self.dic.keys():
			stud = Student(entry.userid)
			stud.add(entry.userid, entry)
			self.dic[entry.userid] = stud
		else:
			self.dic[entry.userid].add(entry.sem_name, entry)

	def get_num_semesters(self, userid):
		return len(self.dic[userid].dic)

	def get_ever_completed_rate(self):
		return sum([item.get_ever_completed() for item in self.dic.values()]) / len(self.dic)

	def deep_copy(self):
		new_cohort = Cohort()
		for student in self.dic.values():
			new_cohort.add(student.userid, student.deep_copy())
		return new_cohort

class SmallGroup(object):

	def __init__(self):
		self.dic = {}

	def add(self, key, value):
		self.dic[key] = value

	def delete(self, value):
		del self.dic[value]

	def get(self, key):
		if key not in self.dic.keys():
			return None
		return self.dic[key]

	def get_keys(self):
		return self.dic.keys()

	def get_num_registered(self):
		return len(self.dic)

	def get_num_viewed(self):
		return sum([1 if entry.viewed else 0 for entry in self.dic.values()])

	def get_num_explored(self):
		return sum([1 if entry.explored else 0 for entry in self.dic.values()])

	def get_num_completed(self):
		return sum([1 if entry.completed else 0 for entry in self.dic.values()])

	def get_completion_rate(self):
		return self.get_num_completed() / len(self.dic)

	def get_award_rate(self):
		num = sum([1 if entry.mode == 'verified' and entry.completed else 0 for entry in self.dic.values()]) 
		den = sum([1 if entry.mode == 'verified' else 0 for entry in self.dic.values()])
		if den == 0:
			return 0
		return num / den

	def get_average(self, stat, complete = False):
		ls = []
		for entry in self.dic.values():
			if (complete and entry.completed) or not complete:
				value = entry.get_stat(stat)
				if value != None:
					ls.append(value)
		if len(ls) == 0:
			return None
		return sum(ls) / len(ls)

	def get_all_entries(self):
		ls = []
		for entity in self.dic.values():
			ls.append(entity)
		return ls


# a collection of Entity objects organized by semester
class Semester(SmallGroup):

	def __init__(self, name, is_1x, is_self_paced, dates_list):
		super().__init__()

		self.name = name
		self.is_1x = is_1x
		self.is_self_paced = is_self_paced
		self.start_date = dates_list[0]
		self.end_date = dates_list[1]
		self.season = dates_list[2]
		self.students = {}

	def __str__(self):
		return str(self.students)

	def deep_copy(self):
		new_sem = Semester(self.name, self.is_1x, self.is_self_paced, [self.start_date, self.end_date, self.season])
		for entry in self.dic.values():
			new_sem.add(entry.userid, entry)
		return new_sem


# a collection of Entry objects organized by student
class Student(SmallGroup):

	def __init__(self, userid):
		super().__init__()
		self.userid = userid

	def get_num_semesters(self):
		return len(self.dic)

	def is_in_semester(self, semester_name):
		return semester_name in self.dic.keys()

	def get_last_semester(self, semester_names):
		last = None
		last_index = None
		for sem_name in self.dic.keys():
			if last_index == None or last_index < semester_names.index(sem_name):
				last = sem_name
				last_index = semester_names.index(sem_name)
		return last

	def get_ever(self, stat):
		for entity in self.dic.values():
			if stat == 'completed' and entity.completed:
				return 1
			elif stat == 'explored' and entity.explored:
				return 1
			elif stat == 'viewed' and entity.viewed:
				return 1
		return 0

	def deep_copy(self):
		new_student = Student(self.userid)
		for entry in self.dic.values():
			new_student.add(entry.sem_name, entry)
		return new_student


class Entry(object):

	def __init__(self, sem_name, userid, username, viewed, explored, certified, completed, 
					education_level, age, gender, grade, start_time, first_event, last_event, 
					num_events, num_active_days, num_forum_events, num_videos, num_problem_checks,
					mode):
		self.sem_name = sem_name
		self.userid = userid
		self.username = username
		self.viewed = viewed
		self.explored = explored
		self.certified = certified
		self.completed = completed
		self.education_level = education_level
		self.age = age
		self.gender = gender
		self.grade = grade
		self.start_time = start_time
		self.first_event = first_event
		self.last_event = last_event
		self.num_events = num_events
		self.num_active_days = num_active_days
		self.num_forum_events = num_forum_events
		self.num_videos = num_videos
		self.num_problem_checks = num_problem_checks
		self.mode = mode
		self.is_cta = False
		self.sem_number = -1

		self.grades = {}

	def get_stat(self, stat):
		value = None
		if stat == 'overall_grade':
			value = self.get_grade()
		elif stat == 'pset':
			value = self.get_pset_average()
		elif stat == 'quiz':
			value = self.get_quiz()
		elif stat == 'final':
			value = self.get_final()
		elif stat == 'active_days':
			value = self.num_active_days
		elif stat == 'forum':
			value = self.num_forum_events
		elif stat == 'videos':
			value = self.num_videos
		elif stat == 'problem_checks':
			value = self.num_problem_checks
		elif stat == 'finger_exercises':
			value = self.get_finger_ex_average()
		elif stat == 'age':
			value = self.age
		elif stat == 'female':
			value = 1 if self.gender == 'f' else 0
		elif stat == 'verified':
			value = 1 if self.mode == 'verified' else 0
		elif stat == 'completed':
			value = 1 if self.completed else 0 
		elif stat == 'viewed':
			value = 1 if self.viewed else 0 

		return value


	def set_grades(self, grades_dic):
		self.grades = grades_dic

	def get_grade(self):
		if self.grades == {}:
			return None
		return self.grades["Grade"]

	def get_finger_ex_average(self):
		if self.grades == {}:
			return None
		if "Finger Exercises (Avg)" in self.grades:
			return self.grades["Finger Exercises (Avg)"]
		if "Lecture Sequence (Avg)" in self.grades:
			return self.grades["Lecture Sequence (Avg)"]

	def get_pset_average(self):
		if self.grades == {}:
			return None
		return self.grades["Problem Set (Avg)"]

	def get_quiz(self):
		if self.grades == {}:
			return None
		if "Quiz" in self.grades:
			return self.grades["Quiz"]
		if "Midterm" in self.grades:
			return self.grades["Midterm"]

	def get_final(self):
		# print (self.grades)
		if self.grades == {}:
			return None
		if "Final" in self.grades:
			return self.grades["Final"]
		if "Final Exam" in self.grades:
			return self.grades["Final Exam"]

	def __str__(self):
		return self.username
