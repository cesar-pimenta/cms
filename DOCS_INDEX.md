# 📚 Documentação - Índice Completo

## 🚀 Começar Aqui

Para iniciantes e overview rápido:

1. **[INFRASTRUCTURE.md](./INFRASTRUCTURE.md)** ⭐
   - O que foi implementado
   - Por que é importante
   - Próximos passos em 45 minutos
   - **Tempo:** 10 min

2. **[DEPLOY_QUICK_START.md](./DEPLOY_QUICK_START.md)**
   - Checklist rápido
   - Comandos essenciais
   - Troubleshooting rápido
   - **Tempo:** 15 min

## 📖 Guias Detalhados

Para implementação completa:

3. **[DIGITALOCEAN_SETUP.md](./DIGITALOCEAN_SETUP.md)**
   - Criar conta DigitalOcean
   - Setup de 3 droplets
   - Configurar Docker
   - Domínio e SSL
   - **Tempo:** 45-60 min

4. **[DEPLOY.md](./DEPLOY.md)**
   - Setup GitHub Actions
   - Configuração de secrets
   - Fluxo de deploy
   - Monitoramento
   - Troubleshooting avançado
   - **Tempo:** 30 min

## 📋 Referência Rápida

### Arquivos Importantes

```
.github/workflows/
├── tests.yml          # Testes automatizados
├── build-docker.yml   # Build das imagens
└── deploy.yml         # Deploy automático

.env.development       # Variáveis dev
.env.staging          # Variáveis staging
.env.production       # Variáveis prod

docker-compose.yml    # Local/dev
docker-compose.prod.yml # Produção otimizado

deploy.sh             # Script de deploy local
config/health.py      # Health check endpoint
```

### Branches

```
main       → Produção (deploy automático)
staging    → Homologação (deploy automático)
develop    → Desenvolvimento (deploy automático)
feature/*  → Features em desenvolvimento
```

## 🎯 Tarefas Comuns

### Desenvolver nova feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/minha-feature
# ... code ...
git push origin feature/minha-feature
# Abrir PR no GitHub
```

### Deploy em staging
```bash
git checkout staging
git merge develop
git push origin staging
# Auto-deploy em STAGING
```

### Deploy em produção
```bash
git checkout main
git merge staging
git push origin main
# Auto-deploy em PROD
```

### Ver logs
```bash
ssh root@seu-droplet-ip
cd /app/cms
docker-compose logs -f django
```

### Health check
```bash
curl https://seu-dominio.com/health/
```

## 🔧 Configuração

### GitHub Secrets Necessários

```
DOCKER_USERNAME        → Seu usuário Docker Hub
DOCKER_PASSWORD        → Token Docker Hub
DO_SSH_KEY            → Chave SSH privada
DO_DROPLET_DEV_IP     → IP droplet desenvolvimento
DO_DROPLET_STAGING_IP → IP droplet staging
DO_DROPLET_PROD_IP    → IP droplet produção
SLACK_WEBHOOK         → (opcional) Notificações Slack
```

### Variáveis de Ambiente

**Desenvolvimento:**
```
DEBUG=True
SECURE_SSL_REDIRECT=False
```

**Staging/Produção:**
```
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 📊 Arquitetura

```
GitHub → Actions → Docker Hub → DigitalOcean
  ↓        ↓          ↓           ↓
Tests   Build    Push Images   Droplets
  ↓        ↓          ↓           ↓
Pass?   Success?   Ready?     Deploy!
```

## 💡 Dicas Importantes

1. **Sempre testar em develop primeiro**
   - Evita quebrar produção
   - GitHub Actions testa automaticamente

2. **Usar SSH keys sem passphrase para deploy**
   - Requisito para automação
   - Segura com GitHub Secrets

3. **Monitorar health check**
   - `/health/` deve retornar 200 OK
   - Indica se app está saudável

4. **Ver logs antes de fazerm PRs**
   ```bash
   docker-compose logs -f django
   ```

5. **Comitar com mensagens claras**
   ```
   git commit -m "Add: descrição breve"
   git commit -m "Fix: bugfix description"
   git commit -m "Refactor: improvements"
   ```

## 🆘 Problemas Comuns

### Deploy falha
- Verificar logs: `docker-compose logs django`
- Verificar health: `curl http://localhost/health/`
- Resetar: `docker-compose down && docker-compose up -d`

### Migration error
```bash
docker-compose exec django python manage.py migrate --verbosity=3
```

### Sem espaço em disco
```bash
docker image prune -a
docker container prune
```

### SSH permission denied
```bash
ssh-copy-id -i ~/.ssh/cms_deploy.pub root@seu-droplet-ip
```

## 📞 Recursos

- **GitHub Actions:** https://docs.github.com/en/actions
- **Docker:** https://docs.docker.com/
- **Django:** https://docs.djangoproject.com/
- **DigitalOcean:** https://docs.digitalocean.com/
- **PostgreSQL:** https://www.postgresql.org/docs/

## ✅ Checklist - Primeiro Deploy

- [ ] Leu INFRASTRUCTURE.md
- [ ] Leu DEPLOY_QUICK_START.md
- [ ] Configurou secrets no GitHub
- [ ] Criou 3 droplets DigitalOcean
- [ ] Instalou Docker em cada droplet
- [ ] Configurou SSH keys
- [ ] Clonando repositório em cada droplet
- [ ] Criou arquivo .env em cada droplet
- [ ] Fez push para develop (teste)
- [ ] GitHub Actions rodou com sucesso
- [ ] App responde em http://seu-droplet-ip
- [ ] Health check retorna 200

## 🎓 Aprendizado Progressivo

**Nível 1 - Iniciante (hoje):**
- Entender o fluxo básico
- Fazer primeiro push
- Ver GitHub Actions executar
- **Tempo:** 2-3 horas

**Nível 2 - Intermediário (1 semana):**
- Entender todos os workflows
- Troubleshoot problemas simples
- Fazer rollback se necessário
- **Tempo:** 10-20 horas

**Nível 3 - Avançado (1-2 meses):**
- Otimizar performance
- Implementar monitoramento
- Adicionar novas features à infraestrutura
- **Tempo:** 20+ horas

## 🚀 Próximas Melhorias

Após ter tudo rodando:
1. Backups automáticos do banco
2. Redis para cache
3. CDN para static files
4. Monitoring com Prometheus
5. Log aggregation com ELK Stack
6. Load balancer
7. Kubernetes (depois, se necessário)

---

**Versão:** 1.0
**Última atualização:** 2025-11-27
**Status:** Pronto para produção ✅
