# prevpoint-metabase
metabase demo for prevention point

Local Setup
-----------------

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
If you run into errors, try running `pip3 install -r requirements.txt`.

Deploying
---------

First, modify the variables at the top of the `Makefile`.

* DM_IP_ADDRESS - IP address for remote instance
* DM_SSH_KEY - ssh key for remote instance
* DOCKER_MACHINE_NAME - a name for the docker machine (can leave unchanged)

Then, run

```
make deploy
```

This will start a postgres database, and metabase service. 
You can access the metabase on http://<DM_IP_ADDRESS>>:3001/setup

