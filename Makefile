build:
	docker build -t ghcr.io/byronmoreno/eras:1.0.5 .

deploy:
	docker stack deploy --with-registry-auth -c stack.yml eras

rm:
	docker stack rm eras