from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q


class Tema(models.Model):
    """Modelo para categorizar editoriais por temas"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return self.nome


class Autor(models.Model):
    """Modelo para autores de editoriais"""
    nome_completo = models.CharField(max_length=200)
    apelido = models.CharField(max_length=100, unique=True)
    resumo = models.TextField(help_text="Breve descrição profissional do autor")
    foto = models.ImageField(upload_to='autores/', blank=True, null=True)
    
    # Redes Sociais
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome_completo']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.nome_completo


class ConfiguracaoSite(models.Model):
    """Modelo para configurações editáveis do site"""
    # Informações Gerais
    nome_site = models.CharField(max_length=200, default='Portal de Notícias')
    tagline = models.CharField(max_length=300, blank=True, help_text="Slogan ou descrição breve do site")
    sobre = models.TextField(help_text="Texto sobre o site que aparece na sidebar dos artigos")
    
    # Contato
    email_contato = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    
    # Redes Sociais do Site
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    
    # Logo
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'

    def __str__(self):
        return self.nome_site

    @staticmethod
    def get_config():
        """Retorna a configuração do site (sempre uma única instância)"""
        config, created = ConfiguracaoSite.objects.get_or_create(pk=1)
        return config


class Editorial(models.Model):
    """Modelo para os editoriais/notícias"""
    LAYOUT_CHOICES = [
        ('layout1', 'Layout 1 - Imagem Grande'),
        ('layout2', 'Layout 2 - Imagens em Coluna'),
        ('layout3', 'Layout 3 - Imagens em Grade'),
    ]

    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('agendado', 'Agendado'),
        ('publicado', 'Publicado'),
        ('desativado', 'Desativado'),
    ]

    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    temas = models.ManyToManyField(Tema, related_name='editoriais')
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True, related_name='editoriais')
    
    # Layouts e estilos
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='layout1')
    estilo = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text='Escolha entre 1 e 3 estilos disponíveis'
    )
    
    # Imagens (até 3)
    imagem1 = models.ImageField(upload_to='editoriais/', blank=True, null=True)
    imagem2 = models.ImageField(upload_to='editoriais/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='editoriais/', blank=True, null=True)
    
    # Publicação
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    # Agendamento
    agendado = models.BooleanField(default=False)
    data_agendada = models.DateTimeField(null=True, blank=True)
    
    # Controle
    ativo = models.BooleanField(default=True)
    visualizacoes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-data_publicacao', '-data_criacao']
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriais'
        indexes = [
            models.Index(fields=['-data_publicacao']),
            models.Index(fields=['status']),
            models.Index(fields=['-visualizacoes']),
        ]

    def __str__(self):
        return self.titulo

    def pode_publicar(self):
        """Verifica se o editorial pode ser publicado"""
        return self.status in ['rascunho', 'agendado']

    def publicar_agora(self):
        """Publica o editorial imediatamente"""
        if self.pode_publicar():
            self.status = 'publicado'
            self.data_publicacao = timezone.now()
            self.agendado = False
            self.save()
            return True
        return False

    def agendar_publicacao(self, data):
        """Agenda a publicação para uma data futura"""
        if data > timezone.now():
            self.status = 'agendado'
            self.data_agendada = data
            self.agendado = True
            self.save()
            return True
        return False

    def desativar(self):
        """Desativa o editorial"""
        self.status = 'desativado'
        self.ativo = False
        self.save()

    def reativar(self):
        """Reativa um editorial desativado"""
        self.ativo = True
        self.status = 'publicado'
        self.save()

    @staticmethod
    def obter_publicados():
        """Retorna apenas editoriais publicados e ativos"""
        return Editorial.objects.filter(
            status='publicado',
            ativo=True,
            data_publicacao__lte=timezone.now()
        ).order_by('-data_publicacao')

    @staticmethod
    def obter_por_tema(tema_slug):
        """Retorna editoriais de um tema específico"""
        return Editorial.obter_publicados().filter(
            temas__slug=tema_slug
        ).distinct()

    @staticmethod
    def buscar(query):
        """Busca em título, texto e temas"""
        return Editorial.obter_publicados().filter(
            Q(titulo__icontains=query) |
            Q(texto__icontains=query) |
            Q(temas__nome__icontains=query)
        ).distinct()

    def dividir_texto_em_3(self):
        """
        Divide o texto em 3 partes aproximadamente iguais para o Layout 2.
        Retorna lista com 3 seções de texto.
        
        Se houver múltiplos parágrafos (separados por \\n\\n), divide por parágrafos.
        Caso contrário, divide por comprimento de caracteres.
        """
        # Remove espaços extras no início e fim
        texto_limpo = self.texto.strip()
        
        # Tenta dividir por parágrafos primeiro
        paragrafos = [p.strip() for p in texto_limpo.split('\n\n') if p.strip()]
        
        if len(paragrafos) > 3:
            # Se tem mais de 3 parágrafos, divide por parágrafos
            partes_por_secao = len(paragrafos) // 3
            resto = len(paragrafos) % 3
            
            secoes = []
            inicio = 0
            
            for i in range(3):
                tamanho = partes_por_secao + (1 if i < resto else 0)
                fim = inicio + tamanho
                
                texto_secao = '\n\n'.join(paragrafos[inicio:fim])
                secoes.append(texto_secao)
                inicio = fim
            
            return secoes
        
        elif len(paragrafos) > 1:
            # Se tem 2 ou 3 parágrafos, usa como está (com padding)
            return paragrafos + [''] * (3 - len(paragrafos))
        
        else:
            # Se é um único parágrafo, divide por caracteres (procurando quebras naturais)
            # Tenta dividir em sentenças (terminadas com . ! ?)
            import re
            sentencas = re.split(r'(?<=[.!?])\s+', texto_limpo)
            
            if len(sentencas) > 3:
                # Divide por sentenças
                partes_por_secao = len(sentencas) // 3
                resto = len(sentencas) % 3
                
                secoes = []
                inicio = 0
                
                for i in range(3):
                    tamanho = partes_por_secao + (1 if i < resto else 0)
                    fim = inicio + tamanho
                    
                    texto_secao = ' '.join(sentencas[inicio:fim])
                    secoes.append(texto_secao)
                    inicio = fim
                
                return secoes
            
            else:
                # Se menos de 3 sentenças, divide por comprimento
                comprimento = len(texto_limpo)
                tamanho_secao = comprimento // 3
                
                secoes = [
                    texto_limpo[0:tamanho_secao].strip(),
                    texto_limpo[tamanho_secao:tamanho_secao*2].strip(),
                    texto_limpo[tamanho_secao*2:].strip()
                ]
                
                return secoes

    def dividir_texto_em_6(self):
        """
        Divide o texto em 5 seções para o Layout 3 (estilo jornal).
        - secoes[0]: Primeiro parágrafo (col-12)
        - secoes[1]: Segundo parágrafo (col-12)
        - secoes[2]: Ao lado da imagem1 (col-6)
        - secoes[3]: Ao lado da imagem2 (col-6)
        - secoes[4]: Ao lado da imagem3 (col-6)
        """
        # Remove espaços extras no início e fim
        texto_limpo = self.texto.strip()
        
        # Tenta dividir por parágrafos primeiro
        paragrafos = [p.strip() for p in texto_limpo.split('\n\n') if p.strip()]
        
        if len(paragrafos) >= 5:
            # Se tem 5 ou mais parágrafos
            return [
                paragrafos[0],                    # Seção 0: primeiro parágrafo
                paragrafos[1],                    # Seção 1: segundo parágrafo
                '\n\n'.join(paragrafos[2:3]),     # Seção 2: com imagem1
                '\n\n'.join(paragrafos[3:4]),     # Seção 3: com imagem2
                '\n\n'.join(paragrafos[4:])       # Seção 4: com imagem3
            ]
        
        elif len(paragrafos) == 4:
            return [paragrafos[0], paragrafos[1], paragrafos[2], '', paragrafos[3]]
        elif len(paragrafos) == 3:
            return [paragrafos[0], paragrafos[1], paragrafos[2], '', '']
        elif len(paragrafos) == 2:
            return [paragrafos[0], paragrafos[1], '', '', '']
        elif len(paragrafos) == 1:
            # Se é um único parágrafo, divide em 5 partes por sentença
            import re
            sentencas = re.split(r'(?<=[.!?])\s+', texto_limpo)
            
            if len(sentencas) >= 5:
                # Distribui as sentenças em 5 seções
                partes_por_secao = len(sentencas) // 5
                resto = len(sentencas) % 5
                
                secoes = []
                inicio = 0
                
                for i in range(5):
                    tamanho = partes_por_secao + (1 if i < resto else 0)
                    fim = inicio + tamanho
                    
                    texto_secao = ' '.join(sentencas[inicio:fim])
                    secoes.append(texto_secao)
                    inicio = fim
                
                return secoes
            else:
                # Se menos de 5 sentenças, divide por comprimento
                comprimento = len(texto_limpo)
                tamanho_secao = comprimento // 5
                
                return [
                    texto_limpo[0:tamanho_secao].strip(),
                    texto_limpo[tamanho_secao:tamanho_secao*2].strip(),
                    texto_limpo[tamanho_secao*2:tamanho_secao*3].strip(),
                    texto_limpo[tamanho_secao*3:tamanho_secao*4].strip(),
                    texto_limpo[tamanho_secao*4:].strip()
                ]
        
        return ['', '', '', '', '']


class Newsletter(models.Model):
    """Modelo para inscrição em notificações por email"""
    email = models.EmailField(unique=True, db_index=True)
    temas = models.ManyToManyField(Tema, related_name='subscribers', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Inscrição Newsletter'
        verbose_name_plural = 'Inscrições Newsletter'

    def __str__(self):
        return f"{self.email} ({self.temas.count()} temas)"
