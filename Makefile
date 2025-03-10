# Define the Docker Compose file
COMPOSE_FILE=docker-compose-local.yaml

up:
	docker compose -f $(COMPOSE_FILE) up --build -d

down:
	docker compose -f $(COMPOSE_FILE) down && docker network prune --force

run:
	docker exec -it fastapi_app uvicorn main:app --host 10.0.1.124 --port 8000 --reload

# Restart the FastAPI service only
restart-fastapi:
	docker compose -f $(COMPOSE_FILE) restart fastapi

# Restart the FastAPI service only
stop-fastapi:
	docker compose -f $(COMPOSE_FILE) stop fastapi

# Restart the database service only
restart-db:
	docker compose -f $(COMPOSE_FILE) restart db

# Rebuild the FastAPI service without using cache
rebuild-fastapi:
	docker compose -f $(COMPOSE_FILE) build --no-cache fastapi

# Rebuild all services
rebuild:
	docker compose -f $(COMPOSE_FILE) up --build -d

# Show logs for the FastAPI service
logs-fastapi:
	docker compose -f $(COMPOSE_FILE) logs -f fastapi

# Show logs for the database service
logs-db:
	docker compose -f $(COMPOSE_FILE) logs -f db

# Run a shell inside the FastAPI container
shell-fastapi:
	docker exec -it fastapi_app /bin/sh

# Run a shell inside the PostgreSQL container
shell-db:
	docker exec -it finance_db psql -U postgres -d finance

# Stop all running containers
stop:
	docker compose -f $(COMPOSE_FILE) stop

# Remove all stopped containers, networks, and volumes
clean:
	docker system prune -af --volumes