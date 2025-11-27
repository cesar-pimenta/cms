# Segurança - Guia de Configuração

## ⚠️ IMPORTANTE: Variáveis de Ambiente

Todas as credenciais sensíveis **DEVEM** ser definidas como variáveis de ambiente antes de executar a aplicação.

### Configuração Local (Desenvolvimento)

1. **Copie o arquivo de exemplo:**
```bash
cp .env.example .env
```

2. **Edite o arquivo `.env` com suas credenciais reais:**
```bash
nano .env
```

3. **NUNCA commit o arquivo `.env`:**
```bash
# Já está no .gitignore
git status  # Não deve aparecer .env
```

### Variáveis Críticas Obrigatórias

```
SECRET_KEY              # OBRIGATÓRIA - Deve ser unique por environment
DB_PASSWORD             # OBRIGATÓRIA - Senha do PostgreSQL
EMAIL_HOST_PASSWORD     # OBRIGATÓRIA - Se usar SMTP
```

### Exemplo de Setup

**Desenvolvimento:**
```bash
cp .env.example .env
# Editar .env com valores de DEV
python manage.py runserver
```

**Docker (local):**
```bash
cp .env.example .env.docker
# Editar com valores
docker-compose up
```

**DigitalOcean (produção):**
```bash
# SSH no droplet
ssh root@seu-droplet

# Criar arquivo .env no servidor
cd /app/cms
nano .env  # Adicionar credenciais

# Iniciar containers
docker-compose up -d
```

## 🔒 Segurança no GitHub

### ✅ Protegido

- ✅ **Arquivos `.env`** - Não versionados (`.gitignore`)
- ✅ **Secrets em Workflows** - Usam `${{ secrets.NOME }}`
- ✅ **Código** - Sem hardcoded credentials
- ✅ **Dependências** - Versões atualizadas

### ⚠️ Atenção

Se acidentalmente fizer commit de um `.env`:

```bash
# Remover imediatamente
git rm .env
git commit -m "Remove accidentally committed .env file"
git push

# Para remover também do histórico (avançado)
# Usar: git filter-branch ou BFG Repo-Cleaner
```

## 📋 Checklist de Segurança

Antes de fazer deploy em produção:

- [ ] Gerar novo SECRET_KEY único por ambiente
- [ ] Mudar todas as senhas padrão
- [ ] Configurar ALLOWED_HOSTS com domínio real
- [ ] Ativar HTTPS (SECURE_SSL_REDIRECT=True)
- [ ] Ativar HSTS (SECURE_HSTS_SECONDS=31536000)
- [ ] Revisar DEBUG (deve ser False)
- [ ] Configurar EMAIL com provedor real
- [ ] Fazer backup do banco de dados
- [ ] Testar em staging primeiro

## 🔐 Gerar SECRET_KEY

Para gerar uma SECRET_KEY segura:

```bash
# Python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Ou usar openssl
openssl rand -hex 32
```

## 📚 Referências

- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)
- [Checklist de Deploy](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Environment Variables Best Practices](https://12factor.net/config)

## 🆘 Dúvidas

Se encontrar qualquer credencial exposta:

1. Revoke imediatamente (mudar senha, regenerar token)
2. Remover do git: `git rm --cached arquivo && git commit`
3. Fazer push: `git push`
4. Informar o time

---

**Versão:** 1.0
**Status:** Em vigor
**Última atualização:** 2025-11-27
