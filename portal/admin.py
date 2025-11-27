from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.contrib import messages
from .models import Tema, Editorial, Autor, ConfiguracaoSite, Newsletter


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ['nome']


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'apelido', 'ativo']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome_completo', 'apelido']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_completo', 'apelido', 'resumo', 'foto')
        }),
        ('Redes Sociais', {
            'fields': ('twitter', 'linkedin', 'instagram', 'facebook', 'website'),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('ativo', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConfiguracaoSite)
class ConfiguracaoSiteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações do Site', {
            'fields': ('nome_site', 'tagline', 'logo', 'sobre')
        }),
        ('Contato', {
            'fields': ('email_contato', 'telefone', 'endereco')
        }),
        ('Redes Sociais', {
            'fields': ('twitter', 'linkedin', 'instagram', 'facebook', 'youtube')
        }),
    )

    def has_add_permission(self, request):
        """Permite apenas uma configuração"""
        return not ConfiguracaoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Impede deleção"""
        return False


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'status_badge', 'layout', 'estilo', 'data_publicacao', 'visualizacoes', 'acoes']
    list_filter = ['status', 'layout', 'estilo', 'autor', 'data_criacao', 'ativo']
    search_fields = ['titulo', 'texto']
    filter_horizontal = ['temas']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'visualizacoes']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'texto', 'temas', 'autor')
        }),
        ('Layout e Estilo', {
            'fields': ('layout', 'estilo')
        }),
        ('Imagens (até 3)', {
            'fields': ('imagem1', 'imagem2', 'imagem3')
        }),
        ('Publicação', {
            'fields': ('status', 'ativo', 'data_publicacao')
        }),
        ('Agendamento', {
            'fields': ('agendado', 'data_agendada'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    actions = ['publicar_agora', 'desativar', 'reativar']

    def status_badge(self, obj):
        """Exibe o status com cores"""
        colors = {
            'rascunho': '#808080',
            'agendado': '#FFA500',
            'publicado': '#008000',
            'desativado': '#FF0000',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def acoes(self, obj):
        """Exibe botões de ação rápida"""
        if obj.status == 'rascunho':
            return format_html(
                '<a class="button" href="#" onclick="return false;">Publicar em breve</a>'
            )
        return '-'
    acoes.short_description = 'Ações'

    def publicar_agora(self, request, queryset):
        """Action para publicar imediatamente"""
        count = 0
        for editorial in queryset:
            if editorial.pode_publicar():
                editorial.publicar_agora()
                count += 1
        self.message_user(request, f'{count} editorial(is) publicado(s).')
    publicar_agora.short_description = 'Publicar agora'

    def desativar(self, request, queryset):
        """Action para desativar editoriais"""
        queryset.update(ativo=False, status='desativado')
        self.message_user(request, 'Editorial(is) desativado(s).')
    desativar.short_description = 'Desativar editorial'

    def reativar(self, request, queryset):
        """Action para reativar editoriais"""
        for editorial in queryset:
            editorial.reativar()
        self.message_user(request, 'Editorial(is) reativado(s).')
    reativar.short_description = 'Reativar editorial'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'temas_display', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em', 'temas']
    search_fields = ['email']
    filter_horizontal = ['temas']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações', {
            'fields': ('email', 'ativo')
        }),
        ('Temas de Interesse', {
            'fields': ('temas',),
            'description': 'Selecione os temas sobre os quais deseja receber notificações'
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    def temas_display(self, obj):
        """Exibe os temas de forma legível"""
        temas_list = obj.temas.all()
        if temas_list:
            return ', '.join([tema.nome for tema in temas_list])
        return '(nenhum tema selecionado)'
    temas_display.short_description = 'Temas'

    actions = ['enviar_notificacao_teste']

    def enviar_notificacao_teste(self, request, queryset):
        """Envia email de teste para inscritos"""
        from django.core.mail import send_mail
        from decouple import config
        
        count = 0
        for subscriber in queryset:
            try:
                send_mail(
                    'Teste de Notificação - Portal de Notícias',
                    'Este é um email de teste. Você está inscrito em nossa newsletter!',
                    config('EMAIL_FROM', default='noreply@portal.com'),
                    [subscriber.email],
                    fail_silently=False,
                )
                count += 1
            except Exception as e:
                self.message_user(request, f'Erro ao enviar para {subscriber.email}: {str(e)}', level=messages.ERROR)
        
        self.message_user(request, f'{count} email(is) de teste enviado(s).')
    enviar_notificacao_teste.short_description = 'Enviar email de teste'
