# Integração DigitalOcean - Passo a Passo

## 🎯 Objetivo

Deploy automático do projeto em 3 ambientes:
- **Development** ($5/mês)
- **Staging** ($5/mês)  
- **Production** ($10-20/mês)

## 📍 Passo 1: Criar Conta DigitalOcean

1. Acesse: https://www.digitalocean.com
2. Sign Up com email
3. Adicione método de pagamento
4. Você ganha $200 em créditos para 60 dias (novo usuário)

## 🖥️ Passo 2: Criar 3 Droplets

### 2.1 Primeiro Droplet (Development)

1. Dashboard → "Create" → "Droplets"
2. **Choose an image:** Ubuntu 22.04 (LTS)
3. **Choose a size:** Basic ($5/month)
   - 1 GB RAM
   - 1 vCPU
   - 25 GB SSD
4. **Datacenter region:** Escolha região mais próxima
5. **Authentication:** SSH Key
   - "New SSH Key"
   - Adicione sua chave pública
   - Se não tiver: `ssh-keygen -t ed25519`
6. **Hostname:** cms-dev
7. Clique "Create Droplet"
8. Aguarde criar (2-3 min)
9. **Anote o IP** (ex: 192.168.1.10)

### 2.2 Segundo Droplet (Staging)

Repetir 2.1 com:
- **Hostname:** cms-staging
- **Anote o IP**

### 2.3 Terceiro Droplet (Production)

1. Repetir 2.1 com:
   - **Size:** Standard ($10/month) OU Basic ($5/month)
   - **Hostname:** cms-prod
   - **Anote o IP**

## 🔐 Passo 3: Adicionar Chave SSH para Deployments

### 3.1 Gerar chave SSH sem passphrase (no seu PC)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/cms_deploy -N ""
```

Responda com ENTER todas as perguntas.

Isso cria:
- `~/.ssh/cms_deploy` (privada - guardar)
- `~/.ssh/cms_deploy.pub` (pública - compartilhar)

### 3.2 Adicionar chave em cada droplet

```bash
# Para cada droplet (dev, staging, prod):
ssh-copy-id -i ~/.ssh/cms_deploy.pub root@seu-droplet-ip

# Ou manualmente:
ssh root@seu-droplet-ip
cat >> ~/.ssh/authorized_keys << EOF
seu-conteudo-de-cms_deploy.pub
EOF
exit
```

### 3.3 Testar acesso SSH

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-ip
# Deve conectar sem pedir senha
exit
```

## 🐳 Passo 4: Configurar Docker em cada Droplet

Execute este script em cada droplet:

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-ip

# Copie e cole:
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install -y docker-compose git curl

# Criar diretório
mkdir -p /app/cms
cd /app/cms

# Clonar repositório
git clone https://github.com/seu-usuario/cms.git .

# Sair
exit
```

## ⚙️ Passo 5: Configurar Ambiente em Cada Droplet

Para cada droplet, prepare o arquivo `.env`:

### Development
```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-dev-ip
cd /app/cms

# Copiar arquivo de exemplo
cp .env.development .env

# Editar
nano .env

# Mudar apenas se necessário:
# DB_PASSWORD=mudepara-senhaForte123
# ALLOWED_HOSTS=seu-ip-ou-dominio

# Verificar que ficou certo
cat .env | head -20

exit
```

### Staging
```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-staging-ip
cd /app/cms

cp .env.staging .env
nano .env

# Adicionar valores reais:
# ALLOWED_HOSTS=staging.seu-dominio.com
# DB_PASSWORD=senhaStaging123
# EMAIL_HOST_USER=seu-email@gmail.com
# EMAIL_HOST_PASSWORD=seu-app-password

exit
```

### Production
```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-prod-ip
cd /app/cms

cp .env.production .env
nano .env

# Adicionar valores reais (muito importante!):
SECRET_KEY=sua-chave-super-secreta-aleatória-64-caracteres
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DB_PASSWORD=senhaProducaoMuitoForte123
SECURE_SSL_REDIRECT=True

exit
```

## 📝 Passo 6: Adicionar Secrets no GitHub

1. Acesse: https://github.com/seu-usuario/cms/settings/secrets/actions
2. Clique "New repository secret"
3. Adicione cada um:

```
DOCKER_USERNAME
Valor: seu-usuario-docker-hub

DOCKER_PASSWORD
Valor: seu-token-docker-hub (não senha!)

DO_SSH_KEY
Valor: (conteúdo completo de ~/.ssh/cms_deploy - PRIVADA!)
cat ~/.ssh/cms_deploy | xclip  # Linux/Mac: pbcopy
# Paste no GitHub

DO_DROPLET_DEV_IP
Valor: 192.168.1.10 (IP do droplet dev)

DO_DROPLET_STAGING_IP
Valor: 192.168.1.11

DO_DROPLET_PROD_IP
Valor: 192.168.1.12

SLACK_WEBHOOK (opcional)
Valor: https://hooks.slack.com/services/...
```

## 🧪 Passo 7: Testar Deploy Automático

### 7.1 Teste em Development

```bash
# No seu PC
git checkout develop
git pull origin develop

# Fazer uma mudança simples
echo "# Deploy Test" >> README.md
git add README.md
git commit -m "Test: CI/CD deployment"
git push origin develop
```

### 7.2 Acompanhar Deploy

1. Acesse: https://github.com/seu-usuario/cms/actions
2. Clique na workflow que acabou de executar
3. Veja os logs em tempo real

Se tudo passar:
- Tests ✅
- Build Docker ✅
- Deploy dev ✅

### 7.3 Verificar no Droplet

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-dev-ip
cd /app/cms

# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f django

# Testar
curl http://localhost/health/
```

## 🌐 Passo 8: Configurar Domínio e SSL

### 8.1 Apontar Domínio para Droplet

1. Provider do domínio (GoDaddy, Namecheap, etc)
2. DNS Manager
3. Adicione ou edite registro A:
   ```
   Host: @
   Type: A
   Value: seu-droplet-prod-ip (ex: 192.168.1.12)
   ```

4. Aguarde propagar (15-30 min)

### 8.2 Configurar SSL (Let's Encrypt)

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-prod-ip

# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obter certificado
certbot certonly --standalone \
  -d seu-dominio.com \
  -d www.seu-dominio.com

# Responda as perguntas e aceite termos

# Conferir
ls -la /etc/letsencrypt/live/seu-dominio.com/
```

### 8.3 Editar nginx.conf

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-prod-ip

# Editar Nginx
nano nginx/default.conf

# Adicione ao final:
server {
    listen 443 ssl http2;
    server_name seu-dominio.com www.seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://django:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Salvar: Ctrl+O, Enter, Ctrl+X
```

### 8.4 Reiniciar

```bash
cd /app/cms
docker-compose restart nginx
```

## 📊 Passo 9: Monitoramento

### Ver Logs em Tempo Real

```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-ip
cd /app/cms

docker-compose logs -f django    # Logs do Django
docker-compose logs -f nginx     # Logs do Nginx
docker-compose logs -f postgres  # Logs do DB
```

### Health Check

```bash
# De qualquer lugar
curl https://seu-dominio.com/health/
# Retorna: {"status": "healthy", "version": "1.0.0"}
```

## 🚀 Fluxo de Produção Completo

### Desenvolver
```bash
git checkout develop
git checkout -b feature/minha-feature
# ... code ...
git push origin feature/minha-feature
# Pull Request em GitHub
# Auto-testa e deploy em DEV
```

### Testar em Staging
```bash
git checkout staging
git pull origin develop
git push origin staging
# Auto-deploy em STAGING
# Teste: https://staging.seu-dominio.com
```

### Ir para Produção
```bash
git tag v1.0.0
git push origin v1.0.0

git checkout main
git merge staging
git push origin main
# Auto-deploy em PRODUÇÃO
# Verificar: https://seu-dominio.com
```

## 🆘 Troubleshooting

### "Permission denied (publickey)"
```bash
# Verificar acesso SSH
ssh -i ~/.ssh/cms_deploy root@seu-droplet-ip

# Se falhar, adicione chave novamente
ssh-copy-id -i ~/.ssh/cms_deploy.pub root@seu-droplet-ip
```

### Deploy falha "Repository not found"
- Verifique se `.git/config` contém credenciais
- Teste: `git remote -v`
- Se tiver token no URL, remova: `git remote set-url origin https://github.com/seu-usuario/cms.git`

### App não responde após deploy
```bash
ssh -i ~/.ssh/cms_deploy root@seu-droplet-ip
cd /app/cms

# Restartar
docker-compose down
docker-compose up -d

# Ver erro
docker-compose logs django | tail -50
```

### Banco de dados não migra
```bash
docker-compose exec django python manage.py migrate --verbosity=3
```

## ✅ Checklist Final

- [ ] 3 Droplets criados (dev, staging, prod)
- [ ] Docker instalado em cada um
- [ ] Repositório clonado em cada um
- [ ] `.env` configurado em cada um
- [ ] SSH key funciona em todos
- [ ] Secrets adicionados no GitHub
- [ ] Primeiro deploy de teste passou
- [ ] Health check retorna 200
- [ ] Domínio aponta para IP correto
- [ ] SSL funcionando
- [ ] Logs podem ser acessados

## 📚 Recursos

- DigitalOcean Docs: https://docs.digitalocean.com/
- Docker Docs: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/en/actions
- Let's Encrypt: https://letsencrypt.org/

## 🎉 Parabéns!

Você tem agora:
- ✅ Infra em 3 ambientes
- ✅ CI/CD automático
- ✅ SSL/HTTPS
- ✅ Health checks
- ✅ Deploy com um push

Você está pronto para produção! 🚀
