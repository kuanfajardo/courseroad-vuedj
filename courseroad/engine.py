import json
from courseroad.models import Subject


#------------------------------#
#     LOGIC CHECK CLASSES      #
#------------------------------#

class Sat:
    def __init__(self, key, count=-1, sat:bool=True):
        self.key = key
        self._sat_dict = {key: sat}

        self._count = count
        self._required = self._count == -1

        self._i = 0

    def __bool__(self):
        return self._sat_dict[self.key]

    def __iter__(self):
        for k, v in self._sat_dict.items():
            yield (k, v)

    def __rand__(self, other):
        return bool(other) and bool(self)

    def __str__(self):
        return str(self.key) + " satisfied: " + str(bool(self)) + "\n" + str(self._sat_dict)

    def __getitem__(self, item):
        return self._sat_dict.get(item, False)

    def update(self, other):
        if type(other) is not Sat:
            raise TypeError("\'other\' param is not a Sat object")

        # Update sat dict
        for key, sat in other:
            if sat:
                self._i += 1

            if key in self._sat_dict:
                if self._sat_dict[key] != sat: # Previously satisfied
                    sat = True

            self._sat_dict.update({key: sat})


    def set(self, value:bool):
        self._sat_dict[self.key] = value

class Checker:
    def __init__(self, req_obj):
        self.req_obj = req_obj

        self._all_subjects = set()
        self._used_subjects = set()

        self._remove = True
        self._checking_path = False

        self._temp_subjects = {}
        self._path_stack = []

    def check(self, subjects:set):
        self._all_subjects = subjects
        return self.req_obj.is_satisfied(self)

    @property
    def subjects(self):
        return self._all_subjects.difference(self._used_subjects)

    def use_subject(self, subject):
        """
        Remove subject only if being used to satisfy req that can't double count (i.e. excluding tags and paths)
        :param subject:
        :return:
        """
        if self._remove:
            self._used_subjects.add(subject)

    # TODO: fix using of subjects in paths (i.e. only 'use' them globally if selecting its path
    def enter_path(self, path_obj):
        self._temp_subjects[path_obj["idd"]] = {}

    def exit_path(self, path_id):
        pass


#---------------------------#
#    REQUIREMENT CLASSES    #
#---------------------------#

class BaseRequirement:
    def __init__(self, req_obj):
        """
        Constructor.

        :param req_obj:
        :return:
        """
        self.type = req_obj["type"]
        self.req_id = req_obj["idd"]
        self.count = req_obj["count"]
        self.required = self.count == -1
        self.name = req_obj["name"] if "name" in req_obj else ""

        if "pid" in req_obj:
            self.path_id = req_obj["pid"]

        self.checker = None
        self._raw_obj = req_obj

    def is_satisfied(self, checker:Checker):
        """
        Determine if requirement is satisfied. TO BE OVERRIDDEN

        :param subjects: set of subjectIDs (strings)
        :param used: set of subjects already used to satisfy other requirements
        :param remove_subjects: if True, will add all subjects used to satisfy requirement to "used"
        :return:
        :rtype:Sat
        """

        pass

    def to_json(self, sat:Sat, indentLevel:int=0, root:bool=False):
        pass

    @classmethod
    def create_row_obj(cls, text, indentLevel, checked, buttonText):
        return {
            "text": text,
            "indentLevel": indentLevel,
            "checked": checked,
            "buttonText": buttonText
        }

    def create_row(self, text:str, indentLevel:int, checked:bool, button:bool=False, buttonText:str=None):
        return {
            "text": text,
            "indentLevel": indentLevel,
            "checked": "y" if checked else "n",
            "buttonText": text if button else buttonText if buttonText else ""
        }

    def create_button_row(self, text:str, indentLevel:int, checked:bool, buttonText:str=None):
        return self.create_row(text, indentLevel, checked, button=True, buttonText=buttonText)

    def create_count_row(self, count:int, indentLevel:int, checked:bool):
        return self.create_row(str(count) + " of:", indentLevel, checked)

    def create_path_row(self, path_index:int, indentLevel:int, checked:bool):
        letter = "ABCDEFGHIJ"[path_index]
        return self.create_row('Path ' + letter, indentLevel, checked)


class ListRequirement(BaseRequirement): # type == "req"
    def __init__(self, req_obj):
        super().__init__(req_obj)

        self.raw_requirements = req_obj["reqs"]
        self.requirements = []

        for req in req_obj["reqs"]:
            self.requirements.append(RequirementFactory.create(req))

    def is_satisfied(self, checker:Checker):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for req in self.requirements:
            req_sat = req.is_satisfied(checker)
            if req_sat:
                ct += 1

            sat.update(req_sat)

            if ct == self.count:
                break

        if self.required:
            sat_val = ct == len(self.requirements)
        else:
            sat_val = ct >= self.count

        sat.set(sat_val)

        return sat

    def to_json(self, sat:Sat, indentLevel:int=0, root:bool=False):
        rows = []
        if not self.required:
            rows += [
                self.create_count_row(self.count, indentLevel, sat[self.req_id])
            ]

            indentLevel += 1

        for req in self.requirements:
            rows += req.to_json(sat, indentLevel)

        if root:
            return {
                "name": self.name,
                "rows": rows
            }

        return rows


class PathRequirement(BaseRequirement): # type == "path"
    def __init__(self, req_obj):
        super().__init__(req_obj)

        self.raw_paths = req_obj["paths"]
        self.paths = []

        for path in req_obj["paths"]:
            self.paths.append(RequirementFactory.create(path))

    def is_satisfied(self, checker:Checker):
        checker._remove = False
        sat = Sat(self.req_id, self.count)

        ct = 0
        for path in self.paths:
            path_sat = path.is_satisfied(checker)
            if path_sat:
                ct += 1

            sat.update(path_sat)

        if self.required:
            sat_val = ct == len(self.paths)
        else:
            sat_val = ct >= self.count

        sat.set(sat_val)

        checker._remove = True
        return sat

    def to_json(self, sat:Sat, indentLevel:int=0, root:bool=False):
        rows = []

        rows += [
            self.create_count_row(self.count, indentLevel, sat[self.req_id])
        ]

        for i, path in enumerate(self.paths):
            rows += [
                self.create_path_row(i, indentLevel + 1, sat[path.req_id])
            ]

            rows += path.to_json(sat, indentLevel + 2)

        if root:
            return {
                "name": self.name,
                "rows": rows
            }

        return rows


class TagRequirement(BaseRequirement): # type == "leaf", has TAG
    def __init__(self, req_obj):
        super().__init__(req_obj)
        self.tag = req_obj["tag"]

    def is_satisfied(self, checker:Checker):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for subject in checker.subjects:
            if True:
                ct += 1

            if ct == self.count:
                break


        sat_val = ct >= self.count
        sat.set(sat_val)

        return sat

    def to_json(self, sat:Sat, indentLevel:int=0, root:bool=False):
        rows = [
            self.create_row(self.tag, indentLevel, sat[self.req_id])
        ]

        if root:
            return {
                "name": self.name,
                "rows": rows
            }

        return rows


class LeafRequirement(BaseRequirement): # type == "leaf", has REQS
    def __init__(self, req_obj):
        super().__init__(req_obj)
        self.requirements = req_obj["reqs"]

    def is_satisfied(self, checker:Checker):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for req in self.requirements:
            if req in checker.subjects:
                ct += 1

            new_sat = Sat(req, sat=req in checker.subjects)
            sat.update(new_sat)

            checker.use_subject(req)

        if self.required:
            sat_val = ct == len(self.requirements)
        else:
            sat_val = ct >= self.count

        sat.set(sat_val)
        return sat

    def to_json(self, sat:Sat, indentLevel:int=0, root:bool=False):
        rows = []
        if not self.required:
            rows += [
                self.create_count_row(self.count, indentLevel, sat[self.req_id])
            ]

            indentLevel += 1

        for req in self.requirements:
            rows += [
                # TODO: create option for "used to satisfy other req"
                self.create_button_row(req, indentLevel, sat[req])
            ]

        if root:
            return {
                "name": self.name,
                "rows": rows
            }

        return rows


#---------------------------#
#     "PUBLIC" CLASSES      #
#---------------------------#

class RequirementFactory:
    @classmethod
    def create(cls, req_obj:object=None, filename:str=None, obj_name:str=None):
        if req_obj is None:
            if filename is not None:
                file_obj = open(str(req_obj))
                req_obj = json.load(file_obj)

            elif obj_name is not None:
                req_obj = {
                    "idd": 0,
                    "name": obj_name,
                    "type": "req",
                    "count": -1,
                    "reqs": []
                }
            else:
                raise ValueError("create(() requires object, filename, or obj_name")

        typ = req_obj["type"]

        if typ == "leaf":
            if "reqs" in req_obj:
                return LeafRequirement(req_obj)
            if "tag" in req_obj:
                return TagRequirement(req_obj)

        if typ == "path":
            return PathRequirement(req_obj)

        if typ == "req":
            return ListRequirement(req_obj)


class Bucket:
    def __init__(self, req_obj:ListRequirement):
        self.req_obj = req_obj
        self.roots = req_obj.requirements

    def check_sat(self, subjects:set):
        sat = Checker(self.req_obj).check(subjects)

        cells = []
        for req in self.roots:
            cells += [
                req.to_json(sat, root=True)
            ]

        return cells

class Road:
    def __init__(self, road:dict, buckets:dict):
        self.road_dict = road
        self.buckets = buckets
        self.subjects = set()

        for year in road.values():
            for semester in year.values():
                for subject in semester:
                    self.subjects.add(subject)

    def check_buckets(self):
        bucket_dict = {bucket: [] for bucket in self.buckets}

        for bucket, req_obj in self.buckets.items():
            cells = Bucket(req_obj).check_sat(self.subjects)
            bucket_dict[bucket] = cells

        return bucket_dict

    def check_pre_reqs(self):
        pre_req_sat = {subject: False for subject in self.subjects}

        already_taken = []
        currently_taking = []

        for year in self.road_dict.values():
            for semester in year.values():
                currently_taking += semester

                for subject in semester:
                    pre_req_sat[subject] = self.sat_req(subject, already_taken, currently_taking)

                already_taken += semester

        return pre_req_sat

    def sat_req(self, subject, already_taken, currently_taking):
        try:
            subject_obj = Subject.objects.get(subjectId=subject)
        except:
            print('SAT REQ ERROR: ' + subject)
            return False
        requisites = json.loads(subject_obj.prerequisites)

        pre_reqs = requisites['pre']
        co_reqs = requisites['co']


        def process_gir(req):
            if req == "Physics I (GIR)":
                req = ['8.01', '8.011', '8.012', '8.01L', 'CC.801', 'CC.8012', 'ES.801', 'ES.8012']
            elif req == "Physics II (GIR)":
                req = ['8.02', '8.021', '8.022', 'CC.802', 'CC.8022', 'ES.802', 'ES.8022']
            elif req == "Biology (GIR)":
                req = ['7.012', '7.013', '7.014', '7.015', '7.016', 'ES.7012', 'ES.7013']
            elif req == "Chemistry (GIR)":
                req = ['3.091', '5.111', '5.112', 'ES.3091', 'ES.5111', 'ES.5112', 'CC.5111']
            elif req == "Calculus I (GIR)":
                req = ['18.01', '18.01A', 'ES.1801', 'ES.181A', 'CC.181A']
            elif req == "Calculus II (GIR)":
                req = ['18.02', '18.022', '18.02A', 'CC.1802', 'CC.182A', 'ES.1802', 'ES.182A']

            return req

        def sat_or(req_list:list, subjects:list):
            for req in req_list:
                if "GIR" in req:
                    gir_sat = sat_or(process_gir(req), subjects)

                    if gir_sat:
                        return True

                if req in subjects:
                    return True

            return False

        def sat_and(req_list:list, subjects:list):
            for req in req_list:
                if "GIR" in req:
                    gir_sat = sat_or(process_gir(req), subjects)

                    if not gir_sat:
                        return False

                else:
                    if req not in subjects:
                        return False

            return True

        def sat_pre_req():
            sat = True
            for clause in pre_reqs:
                clause_type = clause["type"]
                req_list = clause["arr"]

                if clause_type == "or":
                    clause_sat = sat_or(req_list, already_taken)

                    if clause_sat == False:
                        for req in req_list:
                            if "and" in req:
                                req_arr = [x.strip() for x in req.split("and")]
                                clause_sat = sat_and(req_arr, already_taken)

                elif clause_type == "and":
                    clause_sat = sat_and(req_list, already_taken)

                else:
                    clause_sat = False

                sat &= clause_sat

            return sat

        def sat_co_req():
            sat = True
            for clause in co_reqs:
                clause_type = clause["type"]
                req_list = clause["arr"]

                if clause_type == "or":
                    clause_sat = sat_or(req_list, already_taken + currently_taking)

                    if clause_sat == False:
                        for req in req_list:
                            if "and" in req:
                                req_arr = [x.strip() for x in req.split("and")]
                                clause_sat = sat_and(req_arr, already_taken + currently_taking)

                elif clause_type == "and":
                    clause_sat = sat_and(req_list, already_taken + currently_taking)

                else:
                    clause_sat = False

                sat &= clause_sat

            return sat


        return sat_pre_req() and sat_co_req()


#----------------#
#     TESTS      #
#----------------#

def test():
    import pickle

    pickle_file = "courseroad/static/courseroad/6-3.p"
    r = pickle.load(open(pickle_file, 'rb'))
    subj = {'6.01', '6.0001', '6.004', '6.006', '6.009', '6.031'}

    sat = Checker(r).check(subj)

    ##
    # test_obj = r._raw_obj["reqs"][7]
    # print(RequirementFactory.create(test_obj).to_json(sat, root=True))

    ##
    print(Bucket(r).check_sat(subj))


# test()