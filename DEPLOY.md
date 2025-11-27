# Guia de Deploy e CI/CD

## Visão Geral

Este projeto utiliza GitHub Actions para CI/CD com deploy automático em DigitalOcean. Existem 3 ambientes separados:

- **Development** (branch: `develop`)
- **Staging** (branch: `staging`)
- **Production** (branch: `main`)

## GitHub Actions Workflows

### 1. Tests (`tests.yml`)
- Executado em: `push` e `pull_request` em `main` e `develop`
- Testa o código com PostgreSQL real
- Verifica migrations e testes unitários

### 2. Build Docker (`build-docker.yml`)
- Executado em: `push` e `pull_request`
- Build das imagens Django e Nginx
- Push para Docker Hub automaticamente

### 3. Deploy (`deploy.yml`)
- Executado automaticamente quando há push em `main`, `staging` ou `develop`
- Faz deploy em diferentes droplets do DigitalOcean
- Executa migrations e collectstatic
- Notifica via Slack

## Setup no GitHub

### 1. Configurar Secrets

Acesse: https://github.com/seu-usuario/cms/settings/secrets/actions

Adicione os seguintes secrets:

```
DOCKER_USERNAME          # Seu usuário Docker Hub
DOCKER_PASSWORD          # Seu token Docker Hub
DO_SSH_KEY              # Chave SSH privada para DigitalOcean
DO_DROPLET_DEV_IP       # IP do droplet de desenvolvimento
DO_DROPLET_STAGING_IP   # IP do droplet de staging
DO_DROPLET_PROD_IP      # IP do droplet de produção
SLACK_WEBHOOK           # (Opcional) Webhook do Slack para notificações
```

### 2. Configurar Branch Protection

Acesse: https://github.com/seu-usuario/cms/settings/branches

Para branch `main`:
- ✅ Require status checks to pass (tests e build)
- ✅ Dismiss stale pull request approvals
- ✅ Require code reviews

## DigitalOcean Setup

### 1. Criar Droplets

Crie 3 droplets Ubuntu 22.04 (5 USD/mês cada):

```bash
# Tamanho mínimo para começar: Basic ($5/mês)
# 1 GB RAM, 1 vCPU, 25 GB SSD
```

### 2. Configurar Droplet (repetir para cada um)

```bash
# Conectar via SSH
ssh root@your_droplet_ip

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install -y docker-compose

# Criar diretório do app
mkdir -p /app/cms
cd /app/cms

# Clonar repositório
git clone https://github.com/seu-usuario/cms.git .

# Criar arquivo .env apropriado
cp .env.development .env  # ou .env.staging ou .env.production
```

### 3. Configurar SSH Key para Deploy

Gere uma chave SSH **sem passphrase** para o deploy:

```bash
ssh-keygen -t ed25519 -f deploy_key -N ""

# Adicionar chave pública no servidor
cat deploy_key.pub >> ~/.ssh/authorized_keys

# Adicionar chave privada (conteúdo de deploy_key) no GitHub Secret: DO_SSH_KEY
cat deploy_key
```

### 4. Configurar Firewall

```bash
# UFW (se não estiver ativo)
ufw enable
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw allow 5432/tcp # PostgreSQL (apenas interno)
```

### 5. Configurar SSL (Let's Encrypt)

```bash
# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obter certificado
certbot certonly --standalone -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática
certbot renew --dry-run
```

## Fluxo de Deploy

### Desenvolvimento
```bash
# 1. Criar feature branch
git checkout -b feature/minha-feature

# 2. Fazer commits
git add .
git commit -m "Add feature"

# 3. Push para develop
git push origin feature/minha-feature

# 4. Pull Request para develop
# GitHub Actions roda testes automaticamente

# 5. Merge para develop
# GitHub Actions faz deploy em DEV
```

### Staging
```bash
# 1. Merge develop para staging
git checkout staging
git pull origin develop

# 2. Push para staging
git push origin staging

# GitHub Actions faz deploy em STAGING
```

### Produção
```bash
# 1. Criar release
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# 2. Merge main para produção
git checkout main
git pull origin staging

# 3. Push para main
git push origin main

# GitHub Actions faz deploy em PRODUÇÃO
```

## Monitoramento

### Health Check

O endpoint `/health/` retorna status do app:

```bash
curl https://seu-dominio.com/health/
# {"status": "healthy", "version": "1.0.0"}
```

### Logs

```bash
# SSH no droplet
ssh root@droplet_ip

# Ver logs do Docker
docker-compose logs -f django

# Ver logs do Nginx
docker-compose logs -f nginx

# Ver logs do PostgreSQL
docker-compose logs -f postgres
```

### Backup do Banco de Dados

```bash
# Dump do banco
docker-compose exec postgres pg_dump -U postgres cms_prod > backup.sql

# Restaurar
docker-compose exec -T postgres psql -U postgres cms_prod < backup.sql
```

## Troubleshooting

### Deploy falha no health check
```bash
# Verificar se o app está respondendo
curl -v http://localhost/health/

# Verificar logs
docker-compose logs django | tail -50
```

### Migrations falham
```bash
# SSH no droplet
ssh root@droplet_ip
cd /app/cms

# Rodar migration manualmente
docker-compose exec django python manage.py migrate --noinput
```

### Sem espaço em disco
```bash
# Limpar imagens Docker não usadas
docker image prune -a

# Limpar containers parados
docker container prune
```

## Comandos Úteis

```bash
# Deploy local (desenvolvimento)
./deploy.sh development develop

# Deploy local (staging)
./deploy.sh staging staging

# Deploy local (produção)
./deploy.sh production main

# Reiniciar serviços
docker-compose restart

# Parar todos os serviços
docker-compose down

# Ver status dos containers
docker-compose ps
```

## Próximos Passos

1. ✅ Configurar todos os secrets no GitHub
2. ✅ Criar e configurar 3 droplets no DigitalOcean
3. ✅ Gerar e adicionar chaves SSH
4. ✅ Configurar domínios e DNS
5. ✅ Ativar SSL com Let's Encrypt
6. ✅ Testar deploy automático com push para develop

## Suporte

Para dúvidas sobre GitHub Actions: https://docs.github.com/en/actions
Para dúvidas sobre DigitalOcean: https://docs.digitalocean.com/
