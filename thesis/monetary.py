from classes import Course, Cohort, Semester, Student

def split_course(course, index):
	before = Course(course.semester_names[:index], None, course.is_1x)
	after = Course(course.semester_names[index:index+1], None, course.is_1x)
	for i in range(index+1):
		# if i == len(course.semester_names) - 1:
		# 	continue
		name = course.semester_names[i]
		if i < index:
			before.add(name, course.get(name))
		else:
			after.add(name, course.get(name))
	return (before, after)

def increase_cert(course, index):
	before, after = split_course(course, index)
	print(len(after.semester_names))

	print('right before increase', course.get_semester_by_index(index-1).get_average('verified'))
	print('right after increase', course.get_semester_by_index(index).get_average('verified'))

	print('before increase', before.get_average('verified'))
	print('after increase', after.get_average('verified'))

	print('\nbefore increase', before.get_award_rate())
	print('after increase', after.get_award_rate())

def gating(course, index):
	before, after = split_course(course, index)

	print('before gating', before.get_average('verified'))
	print('after gating', after.get_average('verified'))

	print('\nbefore gating', before.get_award_rate())
	print('after gating', after.get_award_rate())

	print('\nbefore gating', before.get_completion_rate())
	print('after gating', after.get_completion_rate())




def main(course_1x, course_2x):
	print("\n------------------------ MONETARY ----------------------\n")
	print('1x results:\n')
	increase_cert(course_1x, 12)

	print('\n2x results:\n')
	increase_cert(course_2x, 8)