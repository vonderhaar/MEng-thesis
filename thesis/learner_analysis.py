import statistics
from collections import defaultdict
from classes import Course, Cohort, Semester, Student
import csv



# REWRITE
def ctas(ctas_1x, ctas_2x):
	print('1x results (CTAs):\n')
	repeat_1x = ctas_individual(ctas_1x)
	print('2x results (CTAs):\n')
	repeat_2x = ctas_individual(ctas_2x)

	forum = []
	forum_single = []
	for cta in repeat_1x:
		for sem in ctas_1x[cta]:
			if sem['number_forum_events'] == 0:
				continue
			if sem['is_CTA'] and (cta in repeat_2x or repeat_1x[cta] >= 2):
				forum.append(sem['number_forum_events'])
			else:
				forum_single.append(sem['number_forum_events'])
	for cta in repeat_1x:
		for sem in ctas_2x[cta]:
			if sem['number_forum_events'] == 0:
				continue
			if sem['is_CTA'] and repeat_2x[cta] >= 2:
				forum.append(sem['number_forum_events'])
			else:
				forum_single.append(sem['number_forum_events'])

	print('average num forum: ', statistics.mean(forum))
	print('average num forum: ', forum)
	print('average num forum: ', statistics.mean(forum_single))
	print('average num forum: ', forum_single)

# REWRITE
def ctas_individual(ctas):
	grades = []
	num_semesters = defaultdict(int)
	took_class = set()
	repeat = 0
	for key in ctas.keys():
		num = 0
		for sem in ctas[key]:
			if sem['completed']:
				grades.append(sem['grade'])
			if not sem['is_CTA']:
				took_class.add(key)
			if sem['is_CTA']:
				num +=1
		if num == 0:
			print(ctas[key])
			print("\n\n")
		if num >= 2:
			repeat +=1
		num_semesters[key] = num
			
	print('average grade if complete: ', statistics.mean(grades))
	print('total number of unique : ', len(ctas.keys()))
	print('total number of took : ', len(took_class))
	print('total number repeat: ', repeat)
	print(num_semesters)

	return num_semesters

def dual_course(course_1x, course_2x):
	both_1x = Cohort()
	both_2x = Cohort()
	both= Cohort()
	only_1x = Cohort()
	only_2x = Cohort()

	learners_1x = course_1x.get_all_userids();
	learners_2x = course_2x.get_all_userids();
	for entry in course_1x.get_all_entries():
		if entry.userid in learners_2x:
			both.add_entry(entry)
			both_1x.add_entry(entry)
		else:
			only_1x.add_entry(entry)
	for entry in course_2x.get_all_entries():
		if entry.userid in learners_1x:
			both.add_entry(entry)
			both_2x.add_entry(entry)
		else:
			only_2x.add_entry(entry)

	print('completion rate:')
	print("both", both.get_completion_rate())
	print("both_1x", both_1x.get_completion_rate())
	print("both_2x", both_2x.get_completion_rate())
	print("only_1x", only_1x.get_completion_rate())
	print("only_2x", only_2x.get_completion_rate())

	print('\never complete rate:')
	print("both", both.get_ever_completed_rate())
	print("both_1x", both_1x.get_ever_completed_rate())
	print("both_2x", both_2x.get_ever_completed_rate())
	print("only_1x", only_1x.get_ever_completed_rate())
	print("only_2x", only_2x.get_ever_completed_rate())

	print('\ngender:')
	print("both", both.get_average('gender'))
	print("both_1x", both_1x.get_average('gender'))
	print("both_2x", both_2x.get_average('gender'))
	print("only_1x", only_1x.get_average('gender'))
	print("only_2x", only_2x.get_average('gender'))

	print('\nactive days:')
	print("both", both.get_average('active_days'))
	print("both_1x", both_1x.get_average('active_days'))
	print("both_2x", both_2x.get_average('active_days'))
	print("only_1x", only_1x.get_average('active_days'))
	print("only_2x", only_2x.get_average('active_days'))

	print('\ngrade:')
	print("both", both.get_average('overall', True))
	print("both_1x", both_1x.get_average('overall', True))
	print("both_2x", both_2x.get_average('overall', True))
	print("only_1x", only_1x.get_average('overall', True))
	print("only_2x", only_2x.get_average('overall', True))

	print('\npercent')	
	print('percent of 1x users who took 2x', len(both.get_all_userids()) / len(course_1x.get_all_userids()))
	print('percent of 2x users who took 1x', len(both.get_all_userids()) / len(course_2x.get_all_userids()))

def certified(course_1x, course_2x):
	cert = Cohort()
	not_cert = Cohort()

	all_entries = []
	if course_1x != None: 
		all_entries.extend(course_1x.get_all_entries())
		print('1x verified total: ', course_1x.get_average('verified', False, True), course_1x.get_num_registered()*course_1x.get_average('verified', False, True))

	if course_2x != None:
		all_entries.extend(course_2x.get_all_entries())
		print('2x verified total: ', course_2x.get_average('verified', False, True), course_2x.get_num_registered()*course_2x.get_average('verified', False, True))

	ls = []
	ls2 = []
	for entry in all_entries:
		if entry.mode == "verified":
			cert.add_entry(entry)
			ls.append(0 if entry.viewed else 1)
		else:
			not_cert.add_entry(entry)
			ls2.append(0 if entry.viewed else 1)


	print('completion among certified:', cert.get_average('completed'))
	print('grade among certified:', cert.get_average('overall_grade', complete = True))
	print('completion among not certified:', not_cert.get_average('completed'))
	print('grade among not certified:', not_cert.get_average('overall_grade', complete = True))

	ext = ""
	if course_1x != None and course_2x == None:
		ext = "1x/"
	elif course_1x == None and course_2x != None:
		ext = "2x/"
	filename = "./visualization/data/" + ext + "certified.csv"
	with open(filename, mode='w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["Verified","NonVerified"])
		writer.writerow([cert.get_average('overall_grade', complete = True)*100, not_cert.get_average('overall_grade', complete = True)*100])
		writer.writerow([cert.get_average('active_days'),not_cert.get_average('active_days')])
		writer.writerow([cert.get_average('videos'),not_cert.get_average('videos')])
		writer.writerow([cert.get_average('forum'),not_cert.get_average('forum')])

	cert1 = Cohort()
	cert2 = Cohort()
	for entry in all_entries:
		if entry.userid in cert.get_keys() and entry.userid in not_cert.get_keys():
			if entry.mode == 'verified':
				cert1.add_entry(entry)
			else:
				cert2.add_entry(entry)

	print('completion among certified1:', cert1.get_average('completed', complete = False, overall = True))
	print('completion among certified2:', cert2.get_average('completed', complete = False, overall = True))




def main(course_1x, course_2x):
	print("------------------------LEARNER ANALYSIS----------------------")
	print('1x results:\n')
	# certified(course_1x, None)

	print('\n\n2x results:\n')

	# certified(None, course_2x)

	print('\n\nboth results:\n')
	# certified(course_1x, course_2x)


