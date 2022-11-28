test:
	docker build --target test --tag test:latest .
	docker run test:latest

prod:
	docker build --target production --tag prod:latest .
	docker run -p 8080:8080 prod:latest