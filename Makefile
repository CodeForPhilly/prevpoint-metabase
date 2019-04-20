start:
	mkdir -p pgdata metabase-data
	docker-compose up

clean:
	mkdir -p pgdata metabase-data
	rm -r pgdata
	rm -r metabase-data
