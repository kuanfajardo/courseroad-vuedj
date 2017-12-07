from courseroad.engine import RequirementFactory
import pickle
import glob


for req_file in glob.iglob('./static/courseroad/*.req'):
    req = RequirementFactory.create(filename=req_file)

    course_number = req_file.split('/')[-1].split('.')[0]
    pickle_file = './static/courseroad/' + course_number + '.p'

    pickle.dump(req, open(pickle_file, 'wb'))