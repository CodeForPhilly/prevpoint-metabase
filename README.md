# prevpoint-metabase
metabase demo for prevention point

Setup
-----

```
# start postgres and metabase
make start
docker-compose up

# seed postgres with mock data
make seed

# run command below to reset database and metabase data
make clean
```

Note: the file `setup_data.py` currently dumps the mock data in via pandas.
If you run into errors, try running `pip3 install requirements.txt`.

