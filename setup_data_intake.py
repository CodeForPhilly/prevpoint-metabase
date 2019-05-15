import pandas as pd
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from faker import Factory
from faker.providers import BaseProvider
import random
import datetime
import timedelta

engine = create_engine("postgresql://metabase:metabase@localhost:5433/metabase")

fake = Factory.create()

def create_session(self):
    # DBSession = sessionmaker()
    # session = DBSession(bind=self.engine)
    # return session
    session_factory = sessionmaker(bind=self.engine)
    Session = scoped_session(session_factory)

    # now all calls to Session() will create a thread-local session
    some_session = Session()
    return some_session

def gettableobject(self, tablename, schemaname=None, raiseerror=False):
    '''I should make this always raise an error'''
    try:
        table = Table(tablename, self.metadata, autoload=True, autoload_with=self.engine, schema=schemaname)
    except NoSuchTableError as e:
        if raiseerror is True:
            raise ValueError('tablename: {0} schemaname: {1} doesnt exist.'.format(tablename, schemaname))
        else:
            return 'tablename: {0} schemaname: {1} doesnt exist.'.format(tablename, schemaname)
    if table.exists():
        return table

def create_profile_rows(num=1):
    output = []
    for x in range(num):
        intake_date = fake.date_between(start_date="-3y", end_date="today")
        ins_status = random.choices(('insured', 'uninsured', 'application pending'), weights=[1.5, 1, 0.5])
        if ins_status != 'uninsured':
            hmo = random.choices((True,None),weights=[1.5,0.5])
            insurance = random.choices(('Health Partners','Keystone First','Aetna Better Health','United Healthcare'))
            ins_id = fake.credit_card_number(card_type=None)
            prior_auth_date = intake_date + timedelta(days=random.randint(90,200))
        else:
            hmo = None
            insurance = None
            ins_id = None
            prior_auth_date = None
        hiv_status = random.choices((True,None),weights=[0.5,1.5])
        if hiv_status is True:
            hiv_care_info = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            hiv_last_app = intake_date - timedelta(days=random.randint(30,160))
            viral_load = random.choices('>1500', '>10000', '>100000', 'Undetectable')
            cd4 = random.choices(True,None)
            #Todo add languadge for cd4 test
        else:
            hiv_care_info = None
            hiv_last_app = None
            viral_load = None
            cd4 = None
        hcv_status = random.choices((True,None),weights=[0.5,1.5])
        if hcv_status is True:
            hcv_care_info = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            hcv_last_app = intake_date - timedelta(days=random.randint(30,160))
            cchange_status = random.choices("waiting",'active','notinvoved')
        output.append({
            "intake_date": intake_date,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=80),
            "ssn": fake.ssn(taxpayer_identification_number_type="SSN"),
            "state": 'PA',
            "city": 'Philadelphia',
            "address": fake.street_address(),
            "intersection": fake.street_name() + ' & ' + fake.street_name(),
            "phone_number": fake.phone_number(),
            "text_optin": random.choices((True,None),weights=[1.75,0.25]),
            "vm_optin": random.choices((True,None),weights=[1.5,0.5]),
            "state_id": random.choices((True,None),weights=[1.7,0.3]),
            "insurance_status":ins_status,
            "hmo": hmo,
            "insurance": insurance,
            "insurance_id": ins_id,
            "prior_auth_date": prior_auth_date,
            "income_source": random.choices('Full Time','Part Time','Cash Assistance'),
            "monthly_income": random.randint(300,1900),
            "housing_status": random.choices('homeless','temporary housing','shelter','has home')
        })
    return output

def create_inurance_rows(num=1):
    output = []
    for x in range(num):

        output.append({
            "insturance_status":  random.choices(('insured', 'uninsured', 'application pending'),weights=[1.5,1,0.5]),

        })
    return output

def create_app_data(x):
    data = pd.DataFrame(create_rows(x))
    data = data.apply(lambda col: pd.to_datetime(col, errors='ignore')
                    if col.dtypes == object
                    else col,
                    axis=0)
    data.to_sql('intake', engine, if_exists = "append",chunksize = 500)
    session = scoped_session(sessionmaker(bind=engine))
    intake_table = session.gettableobject('intake','public')
    intake_index = session.quiry(intake_table.c.index).all
    print(intake_index)


create_app_data(5000)