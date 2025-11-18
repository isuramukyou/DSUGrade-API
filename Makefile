.PHONY: build rebuild up down restart logs ps

build:
	docker compose up --build -d

rebuild:
	docker compose down && docker compose up --build -d

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f api

ps:
	docker compose ps
