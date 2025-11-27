# Instruções Rápidas - GitHub Actions e Deploy

## 📋 Checklist Rápido

### Passo 1: Configurar Secrets no GitHub (2 min)

1. Acesse: https://github.com/seu-usuario/cms/settings/secrets/actions
2. Clique em "New repository secret"
3. Adicione cada secret abaixo:

```
Nome: DOCKER_USERNAME
Valor: seu-usuario-docker

Nome: DOCKER_PASSWORD
Valor: seu-token-docker

Nome: DO_SSH_KEY
Valor: conteúdo da chave privada SSH (sem passphrase)

Nome: DO_DROPLET_DEV_IP
Valor: 1.2.3.4 (IP do droplet dev)

Nome: DO_DROPLET_STAGING_IP
Valor: 1.2.3.5

Nome: DO_DROPLET_PROD_IP
Valor: 1.2.3.6

Nome: SLACK_WEBHOOK (opcional)
Valor: https://hooks.slack.com/services/...
```

### Passo 2: Criar Droplets no DigitalOcean (5 min)

1. Acesse: https://cloud.digitalocean.com
2. "Create" → "Droplets"
3. Escolha:
   - Image: Ubuntu 22.04 LTS
   - Size: Basic ($5/month)
   - Quantity: 3 (dev, staging, prod)

4. Clique em cada droplet e anote o IP

### Passo 3: Setup de Docker em cada Droplet (5 min por droplet)

```bash
# Conectar via SSH
ssh root@seu-droplet-ip

# Executar script de setup
apt update && apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install -y docker-compose git

# Preparar diretório
mkdir -p /app/cms
cd /app/cms
git clone https://github.com/seu-usuario/cms.git .

# Escolher ambiente
# Para DEV:
cp .env.development .env
# Para STAGING:
cp .env.staging .env
# Para PROD:
cp .env.production .env

# Editar .env com valores reais
nano .env

# Testar
docker-compose up -d
docker-compose logs -f django
```

### Passo 4: Configurar SSH para Deploy (3 min)

```bash
# Na sua máquina local
ssh-keygen -t ed25519 -f ~/.ssh/cms_deploy -N ""

# Para cada droplet
ssh-copy-id -i ~/.ssh/cms_deploy.pub root@seu-droplet-ip

# Adicionar no GitHub Secret DO_SSH_KEY
cat ~/.ssh/cms_deploy  # copiar conteúdo
```

### Passo 5: Testar Pipeline Automático (1 min)

```bash
# Na sua máquina local
git checkout develop
echo "test" >> README.md
git add README.md
git commit -m "Test deploy"
git push origin develop

# Assistir em: https://github.com/seu-usuario/cms/actions
# Deve executar: tests → build-docker → deploy
```

## 🎯 Fluxo Diário de Desenvolvimento

### Desenvolver nova feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/minha-feature
# ... fazer mudanças ...
git add .
git commit -m "Add: descrição da feature"
git push origin feature/minha-feature
# Abrir Pull Request no GitHub
# Aguardar testes passarem
# Merge para develop (auto-deploy em DEV)
```

### Subir para staging
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
# Auto-deploy em PRODUÇÃO
```

## 🔍 Monitorando Deployments

### Ver status das workflows
```
https://github.com/seu-usuario/cms/actions
```

### Ver logs do deploy
```bash
# SSH no droplet
ssh root@seu-droplet-ip
cd /app/cms
docker-compose logs -f django
```

### Verificar health
```bash
curl https://seu-dominio.com/health/
```

## 🆘 Troubleshooting Rápido

### "Permission denied" no deploy
- Verifique que a chave SSH está sem passphrase
- Verifique que a chave pública está em `~/.ssh/authorized_keys` no droplet

### "Deploy failed" no GitHub Actions
- Clique na workflow que falhou
- Expanda os logs
- Procure por "Error:" ou "fatal:"

### Aplicação não responde após deploy
```bash
ssh root@seu-droplet-ip
cd /app/cms
docker-compose restart django
docker-compose logs django
```

### Banco de dados não migra
```bash
ssh root@seu-droplet-ip
cd /app/cms
docker-compose exec -T django python manage.py migrate --verbosity=3
```

## 📚 Documentação Completa

Ver arquivo: `DEPLOY.md` (instruções detalhadas e troubleshooting avançado)

## 🚀 Você está pronto!

1. ✅ Todos os workflows estão configurados
2. ✅ Arquivos de ambiente separados (dev, staging, prod)
3. ✅ Deploy automático com GitHub Actions
4. ✅ Health checks integrado
5. ✅ Pronto para produção

Comece com Passo 1 acima e você terá CI/CD completo em 15 minutos!
