import json
# from courseroad.models import Subject


def prepare_output(obj, sat, level=0):
    typ = obj["type"]
    name = obj["name"] if "name" in obj else None
    reqs = obj["reqs"] if "reqs" in obj else None
    idd = obj["idd"]

    str_arr = []
    if typ == "req":
        name_str = name  # assumes each "req" type has a name
        str_arr.append((name_str, level, sat[idd][0]))

        for req in reqs:
            str_arr += prepare_output(req, sat, level + 1)

        return str_arr

    if typ == "leaf":
        ct = obj["count"]
        required = ct == -1
        tag_req = "tag" in obj

        if name:
            str_arr.append((name, level, sat[idd][0]))  # remove Y/N from name level
            level += 1

        if tag_req:
            str_arr.append(("* " + str(ct) + " class tagged as \'" + obj["tag"] + "\'", level, True
                            if sat[idd][0]
                            else False))

            return str_arr

        if required:
            for subject in reqs:
                subj_str = subject
                str_arr.append((subj_str, level, True if sat[subject][0] else False))

            return str_arr

        else:
            tri_str = str(obj["count"]) + " of: "
            for i, option in enumerate(obj["reqs"]):
                tri_str += option

                if i != len(obj["reqs"]) - 1:
                    tri_str += ", "

            str_arr.append((tri_str, level, sat[idd][0]))

            return str_arr

    if typ == "path":
        name_str = name  # assumes each path has a name
        str_arr.append((name_str, level, sat[idd][0]))

        level += 1
        str_arr.append(("1 of:", level, sat[idd][0]))

        for path in obj["paths"]:
            name_str = "PATH " + str(path["pid"])
            str_arr.append((name_str, level + 1, ""))

            for req in path["reqs"]:
                str_arr += prepare_output(req, sat, level + 2)

        return str_arr



class RequirementFactory:
    @classmethod
    def create(cls, req_obj: object):
        if type(req_obj) is str:
            file_obj = open(req_obj)
            req_obj = json.load(file_obj)

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
                if sat != self._sat_dict[key]:
                    raise AssertionError("Conflicting values for same key \'" + key + "\'")

            self._sat_dict.update({key: sat})

        # Update raw sat value
        if self._required:
            self._sat_dict[self.key] &= other
        else:
            self._sat_dict[self.key] = self._i >= self._count

    def to_json(self):
        pass


# class Checker:
#     def __init__(self, req_obj:BaseRequirement):
#         self.req_obj = req_obj
#
#         self._all_subjects = set()
#         self._used_subjects = set()
#         self._remove = False
#
#     def check(self, subjects:set):
#         self.all_subjects = subjects
#         return self.req_obj.is_satisfied(self.subjects)
#
#     @property
#     def subjects(self):
#         return self._all_subjects.difference(self._used_subjects)

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


    def is_satisfied(self, subjects:set, used:set=None, remove_subjects:bool=True):
        """
        Determine if requirement is satisfied. TO BE OVERRIDDEN

        :param subjects: set of subjectIDs (strings)
        :param used: set of subjects already used to satisfy other requirements
        :param remove_subjects: if True, will add all subjects used to satisfy requirement to "used"
        :return:
        :rtype:Sat
        """

        pass


class ListRequirement(BaseRequirement): # type == "req"
    def __init__(self, req_obj):
        super().__init__(req_obj)

        self.raw_requirements = req_obj["reqs"]
        self.requirements = []

        for req in req_obj["reqs"]:
            self.requirements.append(RequirementFactory.create(req))

    def is_satisfied(self, subjects:set):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for req in self.requirements:
            req_sat = req.is_satisfied(subjects)
            if req_sat:
                ct += 1

            sat.update(req_sat)

            if ct == self.count:
                break

        return sat


class PathRequirement(BaseRequirement): # type == "path"
    def __init__(self, req_obj):
        super().__init__(req_obj)

        self.raw_paths = req_obj["paths"]
        self.paths = []

        for path in req_obj["paths"]:
            self.paths.append(RequirementFactory.create(path))

    def is_satisfied(self, subjects:set):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for path in self.paths:
            path_sat = path.is_satisfied(subjects)
            if path_sat:
                ct += 1

            sat.update(path_sat)

        return sat


class TagRequirement(BaseRequirement): # type == "leaf", has TAG
    def __init__(self, req_obj):
        super().__init__(req_obj)
        self.tag = req_obj["tag"]

    def is_satisfied(self, subjects:set):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for subject in subjects:
            if True:
                ct += 1

            if ct == self.count:
                break

        return sat


class LeafRequirement(BaseRequirement): # type == "leaf", has REQS
    def __init__(self, req_obj):
        super().__init__(req_obj)
        self.requirements = req_obj["reqs"]

    def is_satisfied(self, subjects:set):
        sat = Sat(self.req_id, self.count)

        ct = 0
        for req in self.requirements:
            if req in subjects:
                ct += 1

            new_sat = Sat(req, sat=req in subjects)
            sat.update(new_sat)

        return sat


class Road:
    def __init__(self, subjects={}, course=None):
        self.subject_dict = subjects
        self.all_subjects = []

        for year in subjects.values():
            for semester in year.values():
                for subject in semester:
                    self.all_subjects.append(subject)

        self.course = course

    def check_course(self):
        if self.course is None:
            return None

    def check_pre_reqs(self):
        req_sat = {subject: False for subject in self.all_subjects}

        already_taken = []
        currently_taking = []

        for year in self.subject_dict.values():
            for semester in year.values():
                currently_taking += semester
                # print(currently_taking)
                for subject in semester:
                    req_sat[subject] = self.sat_req(subject, already_taken, currently_taking)

                already_taken += semester

        return req_sat

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
