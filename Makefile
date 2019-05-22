DM_IP_ADDRESS=FILL_ME_IN
DM_SSH_KEY=$(HOME)/.ssh/do_rsa
DOCKER_MACHINE_NAME=prevpoint-metabase


start:
	mkdir -p pgdata metabase-data
	docker-compose up

seed:
	python3 setup_data.py

clean:
	mkdir -p pgdata metabase-data
	rm -r pgdata
	rm -r metabase-data

# Deploying to Digital Ocean

machine:
	docker-machine create \
		--driver=generic \
		--generic-ip-address=$(DM_IP_ADDRESS) \
		--generic-ssh-user=root \
		--generic-ssh-key=$(DM_SSH_KEY) \
		--generic-ssh-port=22 \
		$(DOCKER_MACHINE_NAME)

deploy:
	eval $(docker-machine env $(DOCKER_MACHINE_NAME))
	docker-compose up -d

teardown: clean
	docker-machine rm $(DOCKER_MACHINE_NAME)

