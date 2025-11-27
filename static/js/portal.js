// Portal de Notícias - JavaScript customizado

$(document).ready(function() {
    
    // Fechar alerts automaticamente após 5 segundos
    setTimeout(function() {
        $('.alert-messages .alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);

    // Smooth scroll para links internos
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $(this.getAttribute('href'));
        if(target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });

    // Carregar mais notícias com AJAX (opcional)
    $('.load-more-btn').on('click', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        var url = $(this).attr('href');
        
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'html',
            success: function(data) {
                $('.editoriais-container').append(data);
                $('.load-more-btn').remove();
            },
            error: function() {
                alert('Erro ao carregar mais notícias');
            }
        });
    });

    // Highlight de termo de busca nos resultados
    var searchQuery = $('.search-highlight-query').text();
    if(searchQuery) {
        highlightSearchResults(searchQuery);
    }

    // Tooltip do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover do Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

});

/**
 * Highlight do termo de busca nos resultados
 */
function highlightSearchResults(query) {
    if(!query) return;
    
    var regex = new RegExp('(' + query + ')', 'gi');
    
    $('.card-title, .card-text').each(function() {
        var text = $(this).html();
        text = text.replace(regex, '<mark>$1</mark>');
        $(this).html(text);
    });
}

/**
 * Validação de formulário antes de enviar
 */
function validateForm(formId) {
    var form = document.getElementById(formId);
    if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

/**
 * Confirmar exclusão antes de deletar
 */
function confirmDelete(message) {
    return confirm(message || 'Tem certeza que deseja deletar este item?');
}

/**
 * Mostrar loading spinner
 */
function showLoading(selector) {
    $(selector).html('<div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div>');
}

/**
 * Copiar para clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copiado para clipboard!');
    }, function(err) {
        alert('Erro ao copiar: ' + err);
    });
}

/**
 * Formatar data
 */
function formatDate(dateString) {
    var options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

/**
 * Truncar texto
 */
function truncateText(text, length) {
    if(text.length > length) {
        return text.substring(0, length) + '...';
    }
    return text;
}

/**
 * Validar URL
 */
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}
