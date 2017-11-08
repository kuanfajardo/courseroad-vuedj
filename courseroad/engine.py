import json
from courseroad.fancy_print import *
from courseroad.models import Subject
import requests

satt = {}

names = {}
path_keys = {}
path_sat = {}

full_sat = {}
full_path_sat = {}

real_sat = {}
real_path_sat = {}

requ_path_sat = {}

pre_req_master = {}


def tagged(subject: str, tag: str):
    obj = json.load(open("tags.json"))

    if tag not in obj:
        return False

    return subject in obj[tag]


def check(obj, classes):
    ct = obj["count"]
    required = ct == -1

    if required:
        for subject in obj["reqs"]:
            sat_val = subject in classes
            update_sat(subject,
                       sat_val,
                       obj["path"] if "path" in obj else None)

            update_full_sat(subject,
                            [subject] if sat_val else [],
                            obj["path"] if "path" in obj else None)

            update_real_sat(subject,
                            (sat_val, [subject] if sat_val else []),
                            obj["path"] if "path" in obj else None)

        return

    tag_req = "tag" in obj

    co = 0
    sat = []
    for cl in classes:
        if tag_req and tagged(cl, obj["tag"]) or not tag_req and cl in obj["reqs"]:
            co += 1
            sat += [cl]

        if co == ct:
            break

    update_sat(obj["idd"], co >= ct, obj["path"] if "path" in obj else None)
    update_full_sat(obj["idd"], sat, obj["path"] if "path" in obj else None)
    update_real_sat(obj["idd"], (co >= ct, sat), obj["path"] if "path" in obj else None)


def check_req(obj, classes, path=None):
    typ = obj['type']

    if "name" in obj:
        names[obj["idd"]] = obj["name"]

    if is_leaf(obj):
        if path is not None:
            obj.update({'path': path})

            if path[0] not in path_sat:
                path_sat[path[0]] = {}
                full_path_sat[path[0]] = {}
                real_path_sat[path[0]] = {}

            if path[0] not in path_keys:
                path_keys[path[0]] = {}

            if path[1] in path_keys[path[0]]:
                path_keys[path[0]][path[1]].add(obj["idd"])
            else:
                path_keys[path[0]][path[1]] = {obj["idd"]}

        check(obj, classes)
        return

    if typ == 'path':
        for i, path in enumerate(obj['paths']):
            check_req(path, classes, (obj["idd"], path["pid"]))
        return

    for req in obj['reqs']:
        check_req(req, classes, path)


def update_sat(key, val, path=None):
    if path is None:
        satt.update({key: val})
        return

    satt.update({key: val})

    if path[1] in path_sat[path[0]]:
        path_sat[path[0]][path[1]].update({key: val})
    else:
        path_sat[path[0]][path[1]] = {key: val}


def update_full_sat(key, val, path=None):
    if path is None:
        full_sat.update({key: val})
        return

    full_sat.update({key: val})

    if path[1] in full_path_sat[path[0]]:
        full_path_sat[path[0]][path[1]][key] = val
    else:
        full_path_sat[path[0]][path[1]] = {key: val}


def update_real_sat(key, val, path=None):
    if path is None:
        real_sat.update({key: val})
        return

    real_sat.update({key: val})

    if path[1] in real_path_sat[path[0]]:
        real_path_sat[path[0]][path[1]][key] = val
    else:
        real_path_sat[path[0]][path[1]] = {key: val}


def is_leaf(obj):
    return obj["type"] == "leaf"


def eval_path_sat(path_id):
    max_path = -1
    max_ct = -1

    for path, reqs in path_sat[path_id].items():
        ct = 0
        for req, val in reqs.items():
            if val is True:
                ct += 1

        if ct > max_ct:
            max_path = path
            max_ct = ct

    return max_path, max_ct


def eval_all_path_sat():
    all_path_sat = {}
    for path in path_keys:
        all_path_sat[path] = eval_path_sat(path)
        requ_path_sat[path] = all_path_sat[path][0]

    return all_path_sat


def complete_sat(obj):
    typ = obj["type"]

    if typ == "leaf":
        if obj["count"] != -1:
            return

        req_sat = True
        sat = []
        for subject in obj["reqs"]:
            req_sat &= satt[subject]
            sat += full_sat[subject]

        satt[obj["idd"]] = req_sat
        full_sat[obj["idd"]] = sat
        real_sat[obj["idd"]] = (req_sat, sat)

        return

    if typ == "path":
        # selected_path = requ_path_sat[obj["idd"]]
        # complete_sat(obj["paths"][selected_path])

        for path in obj["paths"]:
            complete_sat(path)

        return

    if typ == "req":
        req_sat = True
        sat = []
        for req in obj["reqs"]:
            complete_sat(req)
            req_sat &= satt[req["idd"]]
            sat += full_sat[req["idd"]]

        satt[obj["idd"]] = req_sat
        full_sat[obj["idd"]] = sat
        real_sat[obj["idd"]] = (req_sat, sat)


def ts(obj, sat, level=0):
    typ = obj["type"]
    name = obj["name"] if "name" in obj else None
    reqs = obj["reqs"] if "reqs" in obj else None
    idd = obj["idd"]

    str_arr = []
    if typ == "req":
        name_str = name  # assumes each req has a name
        str_arr.append((name_str, level, sat[idd]))

        for req in reqs:
            str_arr += ts(req, sat, level + 1)

        return str_arr

    if typ == "leaf":
        ct = obj["count"]
        required = ct == -1
        tag_req = "tag" in obj

        if name:
            str_arr.append((name, level, sat[idd]))  # remove Y/N from name level
            level += 1

        if tag_req:
            str_arr.append(("* " + str(ct) + " class tagged as \'" + obj["tag"] + "\'", level, True
                            if sat[idd]
                            else False))

            return str_arr

        if required:
            for subject in reqs:
                subj_str = subject
                str_arr.append((subj_str, level, True if sat[subject] else False))

            return str_arr

        else:
            tri_str = str(obj["count"]) + " of: "
            for i, option in enumerate(obj["reqs"]):
                tri_str += option

                if i != len(obj["reqs"]) - 1:
                    tri_str += ", "

            str_arr.append((tri_str, level, sat[idd]))

            return str_arr

    if typ == "path":
        name_str = name  # assumes each path has a name
        str_arr.append((name_str, level, sat[idd]))

        level += 1
        str_arr.append(("1 of:", level, sat[idd]))

        for path in obj["paths"]:
            name_str = "PATH " + str(path["pid"])
            str_arr.append((name_str, level + 1, ""))

            for req in path["reqs"]:
                str_arr += ts(req, sat, level + 2)

        return str_arr


def cs(str_arr: list):
    print("")
    for str_line in str_arr:
        level = str_line[1]

        if level == 0:
            print_header("+---------------------------------------------------+")
            print_header("{0:^53}".format(str_line[0]))
            print_header("+---------------------------------------------------+")
            continue

        level -= 1

        if level == 0:
            print("\n-------------------------------------\n")
            out_str = "{0:" + str(level * 3 + 1) + "} {1}"
            print_message(out_str.format("", "** " + str_line[0]) + " **")
            print("")
        else:
            out_str = "{0:" + str(level * 3) + "} {1}"

            req_satisfied = str_line[2]
            if req_satisfied:
                print_success(out_str.format("", str_line[0]))
            else:
                print_failure(out_str.format("", str_line[0]))


def run(classes: set, req_file, show_pre_reqs=False):
    obj = json.load(req_file)
    print(obj)
    check_req(obj, classes)

    all_path_sat = eval_all_path_sat()

    for p, sol in all_path_sat.items():
        path_id, _ = sol

        satt.update(path_sat[p][path_id])
        full_sat.update(full_path_sat[p][path_id])
        real_sat.update(real_path_sat[p][path_id])

    complete_sat(obj)
    x = ts(obj, satt)
    cs(x)

    if show_pre_reqs:
        check_all_pre_reqs(classes)


def check_all_pre_reqs(classes: set):
    all_broken_reqs = {}
    for subject in classes:
        broken_pre_reqs = check_pre_req(subject, classes)

        if not broken_pre_reqs:  # all pre reqs satisfied
            continue

        all_broken_reqs[subject] = broken_pre_reqs

    if all_broken_reqs:
        print(bold("\nUnsatisfied Pre-Requisites:\n"))
        for subject, reqs in all_broken_reqs.items():
            print(bold(subject) + ":  " + failure(pre_req_string(reqs)))
    else:
        print(bold("\nAll Pre-Requisites Satisfied!\n"))


def pre_req_string(p: list):
    req_str = ""

    for req in p:
        if len(req) == 1:
            r_s = req[0]
        else:
            r_s = ", ".join(req[:-1])
            r_s += " or " + req[-1]

        req_str += r_s + "; "

    return req_str


def check_pre_req(subject: str, classes: set):
    if subject in pre_req_master:
        return pre_req_master[subject]

    base_url = "https://mit-public.cloudhub.io/coursecatalog/v2/terms/2017FA/subjects/"
    base_url += subject

    headers = {
        "client_id": "897b5d76f69a469cb8138a8300964211",
        "client_secret": "5fee674bAd0A4b228585Bb1870c4E062"
    }

    try:
        req_json = requests.get(base_url, headers=headers).json()["item"]
    except:
        return []

    if req_json["prerequisites"] == "None":
        return True

    all_pre_reqs = parse_pre_reqs(req_json["prerequisites"])
    broken = []
    for pre_req in all_pre_reqs:
        sat = False
        for p in pre_req:
            if p in classes:
                sat = True
                continue

        if not sat:
            broken.append(pre_req)

    pre_req_master[subject] = broken
    return broken


def parse_pre_reqs(pre_req_str):
    pre_reqs = []
    for p in pre_req_str.split("; "):
        pre_req = p.split(", ")

        or_clause = pre_req.pop().split("or ")

        if or_clause[0] == "":
            or_clause.remove("")

        pre_req += [x.strip() for x in or_clause]

        pre_reqs.append(pre_req)

    return pre_reqs



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
        # TODO: HANDLE BAD SUBJECTS
        try:
            subject_obj = Subject.objects.get(subjectId=subject)
        except:
            print(subject)
            raise Exception
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
