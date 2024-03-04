NAMESPACE := airflow2

.PHONY: init up down logs clear events apply pod pf webserver worker scheduler git sync gitkey build

init:
	@docker compose up airflow-init

up:
	@docker compose --profile flower up -d

down:
	@docker compose --profile flower down

logs:
	@docker compose logs -f

clear:
	@docker compose --profile flower down --volumes --remove-orphans
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf logs/* | echo

events:
	@kubectl get events -n $(NAMESPACE)

apply:
	@kubectl apply -k charts/airflow

pod:
	@kubectl get pod -n $(NAMESPACE)

pf:
	@kubectl port-forward svc/airflow-webserver-svc 8080:8080 --namespace $(NAMESPACE)
	
webserver:
	$(eval PODNAME=$(shell bash -c "kubectl get pod -n $(NAMESPACE) | grep webserver | cut -d ' ' -f 1"))
	@kubectl exec -it -n $(NAMESPACE) $(PODNAME) -- bash

worker:
	$(eval PODNAME=$(shell bash -c "kubectl get pod -n $(NAMESPACE) | grep worker | cut -d ' ' -f 1"))
	@kubectl exec -it -n $(NAMESPACE) $(PODNAME) -- bash

scheduler:
	$(eval PODNAME=$(shell bash -c "kubectl get pod -n $(NAMESPACE) | grep scheduler | cut -d ' ' -f 1"))
	@kubectl exec -it -n $(NAMESPACE) $(PODNAME) -- bash

git:
	$(eval PODNAME=$(shell bash -c "kubectl get pod -n $(NAMESPACE) | grep gitsync | cut -d ' ' -f 1"))
	@kubectl logs -n $(NAMESPACE) $(PODNAME)

sync:
	$(eval PODNAME=$(shell bash -c "kubectl get pod -n $(NAMESPACE) | grep gitsync | cut -d ' ' -f 1"))
	@kubectl exec -it -n $(NAMESPACE) $(PODNAME) -- cat /tmp/.ssh/id_rsa
	@kubectl exec -it -n $(NAMESPACE) $(PODNAME) -- cat /tmp/.ssh/known_hosts

gitkey:
	@kubectl create secret generic secret-gitkey --from-file=id_rsa=./charts/secret/id_rsa --from-file=known_hosts=./charts/secret/known_hosts -n ${NAMESPACE}

build:
	@docker build -t airflow-2.8.2-custom:latest -f docker/Dockerfile .