from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Editorial, Tema, Autor, ConfiguracaoSite, Newsletter


def home(request):
    """Página inicial com os últimos editoriais"""
    editoriais = Editorial.obter_publicados()[:10]
    temas = Tema.objects.filter(ativo=True)
    site_config = ConfiguracaoSite.get_config()
    
    context = {
        'editoriais': editoriais,
        'temas': temas,
        'site_config': site_config,
        'pagina_atual': 'home',
    }
    return render(request, 'portal/home.html', context)


def editoriais_por_tema(request, tema_slug):
    """Exibe editoriais de um tema específico"""
    tema = get_object_or_404(Tema, slug=tema_slug, ativo=True)
    editoriais = Editorial.obter_por_tema(tema_slug)
    
    # Paginação
    paginator = Paginator(editoriais, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    temas = Tema.objects.filter(ativo=True)
    
    context = {
        'tema': tema,
        'page_obj': page_obj,
        'editoriais': page_obj.object_list,
        'temas': temas,
        'pagina_atual': 'tema',
    }
    return render(request, 'portal/tema.html', context)


def detalhe_editorial(request, pk):
    """Exibe o detalhe completo de um editorial"""
    editorial = get_object_or_404(Editorial, pk=pk, status='publicado', ativo=True)
    
    # Incrementar visualizações
    editorial.visualizacoes += 1
    editorial.save(update_fields=['visualizacoes'])
    
    # Editoriais relacionados (mesmo tema)
    editoriais_relacionados = Editorial.obter_publicados().filter(
        temas__in=editorial.temas.all()
    ).exclude(pk=editorial.pk)[:4]
    
    temas = Tema.objects.filter(ativo=True)
    site_config = ConfiguracaoSite.get_config()
    
    context = {
        'editorial': editorial,
        'editoriais_relacionados': editoriais_relacionados,
        'temas': temas,
        'site_config': site_config,
        'pagina_atual': 'detalhe',
    }
    return render(request, 'portal/detalhe.html', context)


def buscar(request):
    """Busca de editoriais"""
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        resultados = Editorial.buscar(query)
        
        # Paginação
        paginator = Paginator(resultados, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None
    
    temas = Tema.objects.filter(ativo=True)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'temas': temas,
        'pagina_atual': 'busca',
    }
    return render(request, 'portal/busca.html', context)


def listar_autores(request):
    """Exibe lista de todos os autores"""
    autores = Autor.objects.filter(ativo=True).order_by('nome_completo')
    
    # Paginação
    paginator = Paginator(autores, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    temas = Tema.objects.filter(ativo=True)
    
    context = {
        'page_obj': page_obj,
        'autores': page_obj.object_list,
        'temas': temas,
        'pagina_atual': 'autores',
    }
    return render(request, 'portal/autores.html', context)


def detalhe_autor(request, apelido):
    """Exibe detalhes do autor e seus editoriais"""
    autor = get_object_or_404(Autor, apelido=apelido, ativo=True)
    
    # Editoriais do autor
    editoriais = Editorial.obter_publicados().filter(autor=autor)
    
    # Paginação
    paginator = Paginator(editoriais, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Outros autores (excluir o atual)
    outros_autores = Autor.objects.filter(ativo=True).exclude(pk=autor.pk)
    temas = Tema.objects.filter(ativo=True)
    
    context = {
        'autor': autor,
        'page_obj': page_obj,
        'editoriais': page_obj.object_list,
        'outros_autores': outros_autores,
        'temas': temas,
        'pagina_atual': 'detalhe_autor',
    }
    return render(request, 'portal/detalhe_autor.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def inscrever_newsletter(request):
    """API para inscrição na newsletter"""
    try:
        email = request.POST.get('email', '').strip()
        temas_ids = request.POST.getlist('temas', [])
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email é obrigatório'})
        
        # Verificar se email já existe e está ativo
        try:
            newsletter = Newsletter.objects.get(email=email)
            
            # Se já está ativo, informar que já está assinando
            if newsletter.ativo:
                return JsonResponse({
                    'success': False,
                    'error': 'Este email já está assinando a newsletter.',
                    'already_subscribed': True,
                    'email': email
                })
            
            # Se estava inativo, reativar
            newsletter.ativo = True
            if temas_ids:
                newsletter.temas.set(temas_ids)
            newsletter.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Bem-vindo de volta à nossa newsletter!',
                'created': False
            })
        
        except Newsletter.DoesNotExist:
            # Criar nova inscrição
            newsletter = Newsletter.objects.create(
                email=email,
                ativo=True
            )
            
            # Adicionar temas
            if temas_ids:
                newsletter.temas.set(temas_ids)
            
            return JsonResponse({
                'success': True,
                'message': 'Bem-vindo à nossa newsletter!',
                'created': True
            })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def cancelar_newsletter(request):
    """API para cancelar inscrição na newsletter"""
    try:
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email é obrigatório'})
        
        # Encontrar e desativar inscrição
        try:
            newsletter = Newsletter.objects.get(email=email)
            newsletter.ativo = False
            newsletter.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Sua assinatura foi cancelada. Sentiremos sua falta!'
            })
        except Newsletter.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Email não encontrado na newsletter.'
            })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["GET"])
def listar_temas_api(request):
    """API para listar temas (usado no modal)"""
    temas = Tema.objects.filter(ativo=True).values('id', 'nome')
    return JsonResponse({'temas': list(temas)})
