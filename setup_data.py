import pandas as pd
from sqlalchemy import create_engine
from faker import Factory
from faker.providers import BaseProvider
import random
import datetime
# create sql connection
engine = create_engine("postgresql://metabase:metabase@localhost:5433/metabase")

fake = Factory.create()


class RaceProvider(BaseProvider):
    __provider__ = "race"
    __lang__ = "en_US"

    def race(self):
        race = [u'white caucasian', u'black african american', u'asian pi', u'native american', u'Latino', u'Other']
        return random.choices(race)


fake.add_provider(RaceProvider)


class GenderProvider(BaseProvider):
    __provider__ = "gender"
    __lang__ = "en_US"

    def gender(self):
        gender = [u'male', u'female', u'mtf', u'ftm', u'gender queer']
        return random.choices(gender)


fake.add_provider(GenderProvider)


class AppointmentProvider(BaseProvider):
    __provider__ = "appointment"
    __lang__ = "en_US"

    def appointment(self):
        date = fake.date_between(start_date="-3y", end_date="today")
        start_hours = random.randint(8, 20)
        start_min = random.randint(0, 59)
        start_appt = datetime.datetime.combine(date, datetime.time(start_hours, start_min))
        called_appt = start_appt + datetime.timedelta(minutes=random.randint(20, 120))
        seen = random.choices(('YES', 'NO ANSWER', 'LEFT', 'CAME BACK', ''),weights=[6, 1, 1, 1, 1], k = 10)
        return (start_appt, called_appt, seen)


fake.add_provider(AppointmentProvider)


class ProgramProvider(BaseProvider):
    __provider__ = "program"
    __lang__ = "en_US"

    def program(self):
        program = (u'TESTING', u'CM', u'SSHP', u'LEGAL', u'CRAFT', u'PHAN', u'STEP', u'BIENESTAR', u'SKWC')
        random.choices(program)
        service = {
            'TESTING': ('RAPID', 'CONFIRM', 'NEED RESULTS', 'C-CHANGE', 'SNS'),
            'CM': ('BENEFITS', 'MENTAL HEALTH', 'HOUSING', 'D&A', 'APPT'),
            'SSHP': ('WOUND CARE', 'MEDICAL FORM', 'PHYSICAL', 'FOLLOW UP', 'OTHER:ENTER IN NOTES'),
            'LEGAL': ('BIRTH CERT', 'CONSULT', 'APPT', 'PUBLIC DEF'),
            'CRAFT': ('DETOX', 'INPATIENT', 'IOP', 'SUBOXONE', 'METHADONE'),
            'PHAN': ('BENEFITS', 'FOLLOW UP', 'APPT', 'FOUND THEM!', 'OTHER: ENTER IN NOTES'),
            'STEP': ('APPT: DR BARCLAY', 'APPT: DR SERGE', 'APPT: MOBILE MAT', 'PATIENT/ NO APPT', 'MEDICATION'),
            'BIENESTAR': ('APPT DR. BAMFORD', 'LABWORK', 'FIBROSCAN', 'MCM', 'FOUND THEM!'),
            'SKWC': ('DR. MORALES', 'NEW PATIENT', 'SICK VISIT', 'OTHER')
        }
        s_program = random.choices(program)
        s_services = random.choices(service[s_program[0]])
        return [s_program[0], s_services[0]]


fake.add_provider(ProgramProvider)


def create_rows(num=1):
    output = []
    for x in range(num):
        f_ppackage = fake.program()
        appt_package = fake.appointment()
        output.append({"program": f_ppackage[0],
                       "service": f_ppackage[1],
                       "date": appt_package[0],
                       "uid": fake.password(length=5, special_chars=False, digits=True, lower_case=False),
                       "first_name": fake.first_name(),
                       "last_name": fake.last_name(),
                       "dob": fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=80),
                       "race": fake.race()[0],
                       "gender": fake.gender()[0],
                       "service_staff": fake.name(),
                       "time_called": appt_package[1],
                       "called": appt_package[2][0],
                       "notes": fake.text(max_nb_chars=250, ext_word_list=None)})
    return output

for i in range(9):
    data = pd.DataFrame(create_rows(1000))

    data = data.apply(lambda col: pd.to_datetime(col, errors='ignore')
                  if col.dtypes == object
                  else col,
                  axis=0)

    data.to_sql("prevpoint", engine, if_exists = "append",chunksize = 500)
