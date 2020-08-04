http://45.79.184.134:5005/
docker build -t agni.etl .
docker logs agni_svc_con -f
docker run --env-file=./dev.env agni.etl
docker-compose -f docker-compose-dev.yml up db
docker-compose -f docker-compose-dev.yml up --build app
docker-compose -f docker-compose-dev.yml build app


docker container ls 
docker container rm agni_db_con -f
docker container stop agni_db_con
docker container rm agni_db_con
