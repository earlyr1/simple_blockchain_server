test:
	docker build --target test --tag blockch/test:latest .
	docker run blockch/test:latest

prod:
	docker build --target production --tag blockch/prod:latest .
	docker run -p 8080:8080 blockch/prod:latest