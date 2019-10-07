import pandas as pd
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from faker import Factory
from faker.providers import BaseProvider
import random
import datetime

fake = Factory.create()

class TheAlchemist(object):

    def __init__(self, msi_local=None, msi_remote=None, postengine=None, pandasengine=None, pandasnamespace=None,
                 django_settings_database=None, enginename=None, user=None, password=None, host=None, port=None,
                 dbname=None):
        '''YOU NEED TO REMEMBER THAT != isnt good enough if there are nulls you need to do or is null ALWAYS'''
        self.enginename = enginename  # postgresql+psycopg2
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.pandasengine = pandasengine
        self.postengine = postengine
        self.engine = self.create_engine()
        self.metadata = self.meta_data()
        self.session = self.create_session()

    def create_engine(self):
        """from either django or inputs. right now django settings.db input is for a specific DB
            this is pretty shitty and not that reusable. i need to work on this"""
        # http://nathansnoggin.blogspot.com/2013/11/integrating-sqlalchemy-into-django.html
        if self.pandasengine:
            if self.pandasnamespace:
                return create_engine("pandas://", namespace=self.pandasnamespace)
            else:
                return create_engine("pandas://")
        elif self.postengine:
            db_url = 'postgresql+psycopg2://metabase:metabase@localhost:5499'
            return create_engine(db_url)

    def transaction(self, executestatement):
        # MAKES NEW SESSION TRANSACTION
        sessionnew = self.create_session()
        try:
            sessionnew.execute(executestatement)
            sessionnew.commit()
        except ProgrammingError as e:
            sessionnew.rollback()
            print('rolled back')
            print(e)

    def meta_data(self):
        # inspect the db metadata to build tables with reflect
        meta = MetaData(bind=self.engine)
        meta.reflect()
        return meta

    def create_session(self):
        # DBSession = sessionmaker()
        # session = DBSession(bind=self.engine)
        # return session
        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)

        # now all calls to Session() will create a thread-local session
        some_session = Session()
        return some_session

    def get_table_columns_as_list(self, tablename=None, schemaname=None, tableobject=None, resultproxy=None):
        columns = []
        if resultproxy is not None:
            columnlistq = [col for col in resultproxy.columns]
            # columnlistq += [col for col in pre_rankproxy.columns]
            for col in columnlistq:
                if col.name == '*':
                    continue
                columns.append(col.name)
            return columns

        if tableobject == None:
            table = self.gettableobject(tablename=tablename, schemaname=schemaname)
        else:
            table = tableobject
        # table = Table(tablename, self.metadata, autoload=True, autoload_with=self.engine, schema=schemaname)
        # print table.metadata

        for c in table.c:
            columns.append(c.name)
        # print(columns)
        return columns

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
            prior_auth_date = intake_date + datetime.timedelta(days=random.randint(90,200))
        else:
            hmo = None
            insurance = None
            ins_id = None
            prior_auth_date = None
        hiv_status = random.choices((True,None),weights=[0.5,1.5])[0]
        if hiv_status is True:
            hiv_care_info = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            hiv_last_app = intake_date - datetime.timedelta(days=random.randint(30,160))
            hiv_last_labs = intake_date - datetime.timedelta(days=random.randint(30,160))
            viral_load = random.choices(('>1500', '>10000', '>100000', 'Undetectable'))[0]
            cd4 = random.choices((True,None))[0]
            #Todo add languadge for cd4 test
        else:
            hiv_care_info = None
            hiv_last_app = None
            hiv_last_labs = None
            viral_load = None
            cd4 = None
        hcv_status = random.choices((True,None),weights=[0.5,1.5])[0]
        if hcv_status is True:
            hcv_care_info = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            hcv_last_app = intake_date - datetime.timedelta(days=random.randint(30,160))
            cchange_status = random.choices(("waiting",'active','notinvoved'))[0]
        else:
            hcv_care_info = None
            hcv_last_app = None
            cchange_status = None
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
            "text_optin": random.choices((True,None),weights=[1.75,0.25])[0],
            "vm_optin": random.choices((True,None),weights=[1.5,0.5])[0],
            "state_id": random.choices((True,None),weights=[1.7,0.3])[0],
            "insurance_status":ins_status[0],
            "hmo": hmo[0],
            "insurance": insurance[0],
            "insurance_id": ins_id,
            "prior_auth_date": prior_auth_date,
            "income_source": random.choices(('Full Time','Part Time','Cash Assistance'))[0],
            "monthly_income": random.randint(300,1900),
            "housing_status": random.choices(('homeless','temporary housing','shelter','has home'))[0],
            "hiv_status": hiv_status,
            "hiv care info":hiv_care_info,
            "hiv last appointment":hiv_last_app,
            "hiv last labs": hiv_last_labs,
            "viral load": viral_load,
            "CD4": cd4,
            "HCV Status": hcv_status,
            "HCV Care Info": hcv_care_info,
            "HCV Last App": hcv_last_app,
            "CChange Status": cchange_status,
            "How Many Times Overdosed": random.randint(1, 8),
            "When Last Overdose": intake_date - datetime.timedelta(days=random.randint(30,160)),
            "Who Revived You": random.choices(('My Mom','My Dad','My Brother','My Sister',
                                               fake.first_name()+' '+fake.last_name()))[0]
        })
    return output


def create_substance_info(profile_index):
    substances = []
    substance_int = random.randint(0, 5)
    for x in range(substance_int):
        substance_used = random.choices(('crack/cocaine', 'amphetamines', 'methamphetamines', 'THC',
                                   'methadone', 'opiates', 'PCP', 'barbital', 'benzodiazapines',
                                   'fentanyl', 'oxycodone', 'buprenorphine', 'k2', 'alcohol'))
        use_itorateor = random.choices((' Times a Day',' Times a Week',' Times a Month'))
        use_integer = random.randint(1, 7)
        if substance_used in ['crack/cocaine', 'amphetamines', 'methamphetamines','methadone', 'opiates', 'PCP',
                          'barbital', 'benzodiazapines', 'fentanyl', 'oxycodone', 'buprenorphine', 'k2']:
            method = random.choices(('Smoke','Snort','Intervinously','Orally'))
        elif substance_used == 'alcohol':
            method = 'Orally'
        elif substance_used == 'THC':
            method = 'Smoked'
        else:
            method = 'Unknown'
        substances.append({
            "Profile Index": profile_index,
            "Substance Used":substance_used[0],
            "Freqency Used":str(use_integer)+use_itorateor[0],
            "Method": method,
            "Dependent": random.choices((True,None),[0.2,1.8])
        })
    return substances


def create_medication_list(profle_index,intake_date):
    medications = []
    medication_int = random.randint(0, 5)
    for x in range(medication_int):
        medication_used = random.choices(('Lamivudine','Furosemide','Alprazolam','Loratadine','Omeprazole',
                                          'Cimetidine','Lovastatin','Calcitriol','Carvedilol'))
        med_times_used = random.randint(2,12)
        date_of_last_dose = intake_date - datetime.timedelta(days=random.randint(30,160))
        dosage = 'Test Amount'
        medications.append({"Profile Index": profle_index,
                            "Medication": medication_used[0],
                            "Times Used": med_times_used,
                            "Last Dose": date_of_last_dose,
                            "Dosage": dosage
        })
    return medications



def main():
    postgresdb = TheAlchemist(postengine=True)
    engine = postgresdb.create_engine()
    example = pd.DataFrame(create_profile_rows(5000))
    example.to_sql('prevpoint_step',con=engine,if_exists='replace')
    session = postgresdb.create_session()
    profiles = postgresdb.gettableobject('prevpoint_step','public')
    index = session.query(profiles.c.index,
                          profiles.c.intake_date).all()
    for _ in index:
        med_list = pd.DataFrame(create_medication_list(_[0],_[1]))
        if med_list is not None and _[0] == 1:
            med_list.to_sql('medications', con=engine, if_exists='replace',index=False)
        elif med_list is not None:
            med_list.to_sql('medications', con=engine, if_exists='append',index=False)
        substance_list = pd.DataFrame(create_substance_info(_[0]))
        if substance_list is not None and _[0] == 1:
            substance_list.to_sql('substances', con=engine, if_exists='replace',index=False)
        elif substance_list is not None:
            substance_list.to_sql('substances', con=engine, if_exists='append',index=False)



main()
