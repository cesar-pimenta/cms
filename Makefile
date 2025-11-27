.PHONY: help build up down logs shell migrate createsuperuser backup restore clean

help:
	@echo "CMS Portal - Docker Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make build          - Construir imagens Docker"
	@echo "  make up             - Iniciar containers"
	@echo "  make down           - Parar containers"
	@echo "  make clean          - Remover containers e volumes"
	@echo ""
	@echo "Database:"
	@echo "  make migrate        - Executar migrations"
	@echo "  make createsuperuser - Criar superusuário"
	@echo "  make backup         - Fazer backup do banco"
	@echo "  make restore        - Restaurar backup"
	@echo ""
	@echo "Development:"
	@echo "  make logs           - Ver logs em tempo real"
	@echo "  make shell          - Abrir Django shell"
	@echo "  make django-cmd CMD=<comando> - Executar comando no Django"
	@echo ""
	@echo "Monitoring:"
	@echo "  make ps             - Ver status dos containers"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Aplicação iniciada!"
	@echo "   Site: http://localhost"
	@echo "   Admin: http://localhost/admin"

down:
	docker-compose down

clean:
	docker-compose down -v
	@echo "✅ Containers e volumes removidos"

logs:
	docker-compose logs -f

ps:
	docker-compose ps

shell:
	docker-compose exec django python manage.py shell

migrate:
	docker-compose exec django python manage.py migrate

createsuperuser:
	docker-compose exec django python manage.py createsuperuser

django-cmd:
	docker-compose exec django python manage.py $(CMD)

backup:
	docker-compose exec postgres pg_dump -U postgres cms_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup criado"

restore:
	@read -p "Digite o arquivo de backup: " backup; \
	cat $$backup | docker-compose exec -T postgres psql -U postgres cms_db
	@echo "✅ Backup restaurado"

collectstatic:
	docker-compose exec django python manage.py collectstatic --noinput

test:
	docker-compose exec django python manage.py test

lint:
	docker-compose exec django flake8 .

format:
	docker-compose exec django black .

healthcheck:
	@echo "Verificando saúde dos containers..."
	@docker-compose ps
	@echo ""
	@echo "Testando conectividade..."
	@curl -s http://localhost/health/ && echo "✅ Nginx respondendo" || echo "❌ Nginx não respondendo"
	@curl -s http://localhost/api/temas/ && echo "✅ Django respondendo" || echo "❌ Django não respondendo"
