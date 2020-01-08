import sys
from load_data import make_course_run_dates, load_dictionaries, make_repeaters
from classes import Course, Cohort, Semester, Student
from collections import defaultdict
import clean_data
import classes
import load_data
import monetary
import repeaters
import general
import self_vs_instructor
import learner_analysis
import generate_csvs
import importlib
import traceback

course_names_1x = ['1x_3T2013', '1x_2T2014', '1x_3T2014', '1x_1T2015', '1x_2T2015', '1x_3T2015', '1x_1T2016', '1x_2T2016', '1x_3T2016', '1x_1T2017', '1x_2T2017', '1x_3T2017', '1x_2T2018', '1x_1T2019', '1x_2T2019', '1x_3T2019']
course_names_2x = ['2x_1T2014', '2x_3T2014', '2x_1T2015', '2x_3T2015', '2x_1T2016', '2x_3T2016', '2x_1T2017', '2x_3T2017', '2x_3T2018', '2x_1T2019', '2x_3T2019']
self_paced_1x = '1x_3T2017'
self_paced_2x = '2x_3T2017'

promo_1x = defaultdict(int)
promo_1x['1x_2T2016_2'] = 3
promo_1x['1x_1T2017'] = 3
promo_1x['1x_2T2017'] = 3
promo_1x['1x_2T2017_2'] = 19
promo_1x['1x_2T2018'] = 2
promo_1x['1x_1T2019'] = 1
promo_1x['1x_2T2019'] = 3
promo_1x['1x_2T2019a'] = 4
promo_2x = defaultdict(int)
promo_2x['2x_1T2017'] = 1
promo_2x['2x_3T2017'] = 2
promo_2x['2x_3T2018'] = 1

course_1x_raw = Course(course_names_1x, self_paced_1x, True,  promo_1x)
course_2x_raw = Course(course_names_2x, self_paced_2x, False,  promo_2x)
reclean = True
loaded = False

while True:
	try:
		# Load and clean data
		if not loaded:
			load_dictionaries(course_1x_raw)
			load_dictionaries(course_2x_raw)
			loaded = True
		if reclean:
			course_1x = clean_data.clean(course_1x_raw)
			course_2x = clean_data.clean(course_2x_raw)

			repeaters_1x = make_repeaters(course_1x)
			repeaters_2x = make_repeaters(course_2x)
		# Perform analysis
		repeaters.main(course_1x, course_2x, repeaters_1x, repeaters_2x)
		self_vs_instructor.main(course_1x, course_2x, repeaters_1x, repeaters_2x)
		general.main(course_1x, course_2x)
		monetary.main(course_1x, course_2x)
		generate_csvs.main(course_1x, course_2x, repeaters_1x, repeaters_2x)
		learner_analysis.main(course_1x, course_2x)

	except Exception:
		traceback.print_exc()

	response = input("\n\nEnter R to use reclean, any other key to rerun, CTRL-C to exit: ")
	reclean = True if response.upper() == 'R' else False
	importlib.reload(classes)
	importlib.reload(general)
	importlib.reload(repeaters)
	importlib.reload(self_vs_instructor)
	importlib.reload(learner_analysis)
	importlib.reload(monetary)
	importlib.reload(generate_csvs)
	if reclean:
		importlib.reload(clean_data)
