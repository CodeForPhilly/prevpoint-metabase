import pandas as pd
from sqlalchemy import create_engine

# create sql connection
engine = create_engine("postgresql://metabase:metabase@localhost:5433/metabase")

# insert data (note: schema will be largely string columns)
data = pd.read_csv("./hrsc_fake.csv")
data.to_sql("prevpoint", engine, if_exists = "replace")
