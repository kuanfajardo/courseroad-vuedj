from courseroad.signals import signals
from django.db.models.signals import post_init, post_save

from django.dispatch import receiver

from courseroad import engine, models

import pickle


@receiver(post_save, sender=models.User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        num_years = 4
        num_semesters = 3

        # TODO: split this into separate handler for post_init of Semester and Year
        year_titles = ['Freshman', 'Sophomore', 'Junior', 'Senior']
        semester_types = ['fall', 'iap', 'spring']

        for i in range(num_years):
            year = models.Year.objects.create(user=instance, year_id=i, title=year_titles[i])
            for j in range(num_semesters):
                models.Semester.objects.create(year=year, semester_id=j, type=semester_types[j])


@receiver(post_init, sender=models.Bucket)
def create_bucket(sender, instance, **kwargs):
    # Will have name, type, index, custom - need to insert json and req_obj; user in update_fields
    pickle_file = 'courseroad/static/courseroad/' + instance.name + '.p'

    try:
        print(pickle_file)
        req_obj = pickle.load(open(pickle_file, 'rb'))
    except:
        req_obj = engine.RequirementFactory.create(obj_name=instance.name)

    json = engine.Bucket(req_obj, instance.index, instance.custom).check_sat(set())

    instance.json = json
    instance.requirement_obj = req_obj