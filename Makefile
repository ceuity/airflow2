init:
	@docker-compose up airflow-init

up:
	@docker-compose up -d

down:
	@docker-compose down

clear:
	@docker-compose down --volumes --remove-orphans

events:
	@kubectl get events -n airflow-steach2

postgres:
	docker run -d --env-file .env -p 5432:5432 --name postgres postgres:13

redis:
	docker run -d --env-file .env -p 6379:6379 --name redis redis:latest

webserver:
	docker run --env-file .env -p 8080:8080 --link postgres:postgres --link redis:redis --name webserver apache/airflow:2.2.2 webserver

init:
	docker run --env-file .env -p 8080:8080 --link postgres:postgres --link redis:redis --name webserver apache/airflow:2.2.2 db init