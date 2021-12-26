init:
	@docker-compose up airflow-init

up:
	@docker-compose up -d

down:
	@docker-compose down

clear:
	@docker-compose down --volumes --remove-orphans

events:
	@kubectl get events -n airflow2

charts:
	@kubectl apply -k charts/airflow

pod:
	@kubectl get pod -n airflow2

pf:
	@kubectl port-forward svc/airflow-webserver-svc 8080:8080 --namespace airflow2
