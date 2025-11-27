# Portal de Notícias - Django CMS

Portal de notícias desenvolvido com Django com funcionalidades de gerenciamento administrativo, agendamento de publicações e múltiplos layouts.

## Requisitos

- Python 3.8+
- Django 5.2.8
- PostgreSQL

## Instalação

```bash
cd /home/cesar/projects/cms
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse em: `http://localhost:8000` (portal) e `http://localhost:8000/admin` (admin)

## Docker

```bash
docker-compose up
```

## Estrutura

```
portal/
├── models.py          # Modelos: Tema, Autor, Editorial
├── views.py           # Views públicas
├── admin.py           # Configuração do admin
├── management/        # Comandos: popular_dados
└── urls.py            # Roteamento

templates/             # Templates HTML
static/               # CSS, JS e imagens
```
│   └── images/           # Imagens
├── media/                # Uploads de imagens
├── db.sqlite3            # Banco de dados
└── manage.py             # Gerenciador Django
```

## 📝 Modelos

### Tema
```python
- nome: CharField
- descricao: TextField (opcional)
- slug: SlugField (único)
- ativo: BooleanField
- criado_em: DateTimeField
- atualizado_em: DateTimeField
```

### Editorial
```python
- titulo: CharField
- texto: TextField
- temas: ManyToManyField(Tema)
- layout: CharField (layout1, layout2, layout3)
- estilo: IntegerField (1-3)
- imagem1, imagem2, imagem3: ImageField
- status: CharField (rascunho, agendado, publicado, desativado)
- data_publicacao: DateTimeField
- data_criacao: DateTimeField
- data_atualizacao: DateTimeField
- agendado: BooleanField
- data_agendada: DateTimeField
- ativo: BooleanField
- visualizacoes: IntegerField
```

## 🎨 Layouts Disponíveis

### Layout 1 - Imagem Grande
Exibe uma imagem grande no topo do editorial

### Layout 2 - Imagens em Coluna
Exibe as imagens em coluna ao lado esquerdo do texto

### Layout 3 - Imagens em Grade
Exibe as imagens em uma grade de 3 colunas acima do texto

## 🎨 Estilos Disponíveis

### Estilo 1
Fundo branco simples

### Estilo 2
Fundo com gradiente azul e borda na esquerda

### Estilo 3
Fundo branco com borda vermelha

## 🔍 Funcionalidades de Busca

A busca permite encontrar editoriais por:
- **Título**: Busca no campo de título
- **Conteúdo**: Busca em qualquer palavra do texto
- **Tema**: Busca pelo nome do tema associado

A busca é case-insensitive e usa lookup `icontains` do Django ORM.

## 📅 Agendamento de Publicações

1. Crie um editorial com status "Rascunho"
2. Marque a opção "Agendado"
3. Selecione a data e hora desejada
4. O editorial será automaticamente publicado na data especificada

## 🛠️ Personalização

### Cores
Edite as variáveis CSS em `templates/portal/base.html`:
```css
--primary-color: #2c3e50;
--secondary-color: #3498db;
--accent-color: #e74c3c;
--dark-bg: #ecf0f1;
```

### Adicionar CSS Customizado
Crie arquivos em `static/css/` e inclua em `base.html`

### Adicionar JavaScript
Use jQuery incluído no projeto ou adicione seus próprios scripts em `static/js/`

## 📦 Como Usar

### 1. Adicionar um Tema

1. Acesse `/admin`
2. Clique em "Temas"
3. Clique em "Adicionar tema"
4. Preencha os campos e salve

### 2. Criar um Editorial

1. Acesse `/admin`
2. Clique em "Editoriais"
3. Clique em "Adicionar editorial"
4. Preencha:
   - **Título**: Nome do editorial
   - **Texto**: Conteúdo principal
   - **Temas**: Selecione 1 ou mais temas
   - **Layout**: Escolha o layout (1, 2 ou 3)
   - **Estilo**: Escolha o estilo (1, 2 ou 3)
   - **Imagens**: Upload de até 3 imagens
   - **Status**: Rascunho, Agendado ou Publicado

### 3. Agendar uma Publicação

1. Crie o editorial como "Rascunho"
2. Marque "Agendado"
3. Escolha a "Data agendada"
4. Salve
5. O editorial será publicado automaticamente na data escolhida

### 4. Buscar Editoriais

1. Use a barra de busca no topo do portal
2. Digite a palavra-chave
3. Os resultados filtrarão por título, conteúdo ou tema

## 📱 Responsividade

O portal é totalmente responsivo e funciona em:
- Desktop
- Tablet
- Mobile

## 🔐 Segurança

- CSRF Protection habilitado
- SQL Injection prevention via ORM Django
- XSS Protection via template escaping
- Senhas armazenadas de forma segura

## 🚀 Produção

Antes de implantar em produção:

1. Defina `DEBUG = False` em `config/settings.py`
2. Configure `ALLOWED_HOSTS` apropriadamente
3. Use uma SECRET_KEY forte
4. Configure um banco de dados de produção (PostgreSQL, MySQL)
5. Configure STATIC_ROOT e MEDIA_ROOT
6. Use um servidor WSGI (Gunicorn, uWSGI)
7. Configure HTTPS
8. Use um reverse proxy (Nginx, Apache)

## 📧 Suporte

Para dúvidas ou problemas, verifique a documentação do Django:
- https://docs.djangoproject.com/
- https://getbootstrap.com/
- https://jquery.com/

## 📄 Licença

Este projeto é fornecido como está para uso educacional e comercial.

---

**Desenvolvido com ❤️ usando Django, Bootstrap e jQuery**
