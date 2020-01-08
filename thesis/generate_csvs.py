import csv
from collections import defaultdict

def get_promo_data(course, filename):
	print(course.promo_dict)
	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		writer.writerow(["Semester","Registered","TotalPromo"])

		for semester in course.semester_names:
			if course.promo_dict[semester] == 0:
				continue
			registered = course.get(semester).get_num_registered()
			writer.writerow([semester, registered, course.promo_dict[semester]])


def get_engagement(course, filename):
	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		writer.writerow(["Semester","ViewedPercent","ExploredPercent","CompletedPercent","Registered","Viewed","Explored","Completed"])
		for semester in course.semester_names:
			registered = course.get(semester).get_num_registered()
			viewed = course.get(semester).get_num_viewed()
			explored = course.get(semester).get_num_explored()
			completed = course.get(semester).get_num_completed()

			writer.writerow([semester, round(viewed/registered, 3), round(explored/registered,3), round(completed/registered, 3),
							registered, viewed, explored, completed])


def get_grades(course, filename):
	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		writer.writerow(["PsetAvg","ExamAvg"])
		for entry in course.get_all_entries():
			if not entry.completed or entry.grades == {} or entry.get_quiz() == None or entry.get_final() == None or entry.get_pset_average() == None:
				continue

			exam_avg = (entry.get_quiz() + entry.get_final()) / 2
			writer.writerow([entry.get_pset_average(), exam_avg])


def get_gender(course, filename):

	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		writer.writerow(["Semester","Male","Female"])
		for semester in course.semester_names:
			female = course.get(semester).get_average('female')
			male = 1.0 - female
			writer.writerow([semester, round(male,3), round(female, 3)])


def get_education(course, filename):
	edu_dict = {
		"m": "Masters",
		"b": "Bachelors",
		"el": "Elementary school",
		"hs": "High school",
		"jhs": "Junior high school",
		"p": "PhD",
		"p_oth": "p_oth",
		"p_se": "p_se",
		"other": "Other",
		"a": "Associates",
	}

	d = defaultdict(int)
	for entry in course.get_all_entries():
		if entry.education_level != None and entry.education_level != "none" and entry.education_level != "null":
			d[edu_dict[entry.education_level]] += 1

	with open(filename, mode='w') as file:
		writer = csv.DictWriter(file, d.keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		writer.writeheader()
		writer.writerow(d)



def get_age(course, filename1, filename2):
	d = defaultdict(int)
	for entry in course.get_all_entries():
		age = entry.age
		if age == None:
			continue
		if 11 <= age <= 15:
			d["11-15"] += 1
		if 16 <= age <= 20:
			d["16-20"] += 1
		if 21 <= age <= 25:
			d["21-25"] += 1
		if 26 <= age <= 30:
			d["26-30"] += 1
		if 31 <= age <= 35:
			d["31-35"] += 1
		if 36 <= age <= 40:
			d["36-40"] += 1
		if 41 <= age <= 45:
			d["41-45"] += 1
		if 46 <= age <= 50:
			d["46-50"] += 1
		if 51 <= age <= 55:
			d["51-55"] += 1
		if 56 <= age <= 60:
			d["56-60"] += 1
		if 61 <= age <= 65:
			d["61-65"] += 1
		if 66 <= age <= 70:
			d["66-70"] += 1
		if 71 <= age <= 75:
			d["71-75"] += 1

	total = sum([d[key] for key in d])

	with open(filename1, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Range","Number"])
		# sorted_keys = ls(d.keys()).sort()
		for key in sorted(list(d.keys())):
			writer.writerow([key, round(d[key]/total, 3)])

	with open(filename2, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Semester"] + sorted(list(d.keys())))
		# sorted_keys = ls(d.keys()).sort()
		for semester in course.semester_names:
			d = defaultdict(int)
			for entry in course.get(semester).get_all_entries():
				age = entry.age
				if age == None:
					continue
				if 11 <= age <= 15:
					d["11-15"] += 1
				if 16 <= age <= 20:
					d["16-20"] += 1
				if 21 <= age <= 25:
					d["21-25"] += 1
				if 26 <= age <= 30:
					d["26-30"] += 1
				if 31 <= age <= 35:
					d["31-35"] += 1
				if 36 <= age <= 40:
					d["36-40"] += 1
				if 41 <= age <= 45:
					d["41-45"] += 1
				if 46 <= age <= 50:
					d["46-50"] += 1
				if 51 <= age <= 55:
					d["51-55"] += 1
				if 56 <= age <= 60:
					d["56-60"] += 1
				if 61 <= age <= 65:
					d["61-65"] += 1
				if 66 <= age <= 70:
					d["66-70"] += 1
				if 71 <= age <= 75:
					d["71-75"] += 1

			total = sum([d[key] for key in d])
			ls = [round(d[x]/total,3) for x in sorted(list(d.keys()))]

			writer.writerow([semester] + ls)

def main(course_1x, course_2x, repeaters_1x, repeaters_2x):
	print("\n------------------------ GENERATE CSVs ----------------------\n")
	# get_gender(course_1x, './visualization/data/1x/gender.csv')
	# get_gender(course_2x, './visualization/data/2x/gender.csv')
	# get_age(course_1x, './visualization/data/1x/age.csv', './visualization/data/1x/age_semester.csv')
	# get_age(course_2x, './visualization/data/2x/age.csv', './visualization/data/2x/age_semester.csv')
	# get_education(course_1x, './visualization/data/1x/education.csv')
	# get_education(course_2x, './visualization/data/2x/education.csv')
	# get_grades(course_1x, './visualization/data/1x/grades.csv')
	# get_grades(course_2x, './visualization/data/2x/grades.csv')

	# do these when those who never viewed have NOT beeen removed
	# get_promo_data(course_1x, './visualization/data/1x/promo.csv')
	# get_promo_data(course_2x, './visualization/data/2x/promo.csv')
	# get_engagement(course_1x, './visualization/data/1x/engagement.csv')
	# get_engagement(course_2x, './visualization/data/2x/engagement.csv')


