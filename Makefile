start:
	mkdir -p pgdata metabase-data
	docker-compose up

seed:
	python3 setup_data.py

clean:
	mkdir -p pgdata metabase-data
	rm -r pgdata
	rm -r metabase-data
