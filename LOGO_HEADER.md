# Logo Header - Documentação

## Visão Geral

O Logo Header é um componente de marca profissional que aparece no topo da página inicial (homepage) do portal de notícias. Ele fornece destaque visual para o logo e nome da empresa, desaparecendo dinamicamente ao rolar para baixo e reaparecendo ao rolar para cima.

## Características

✅ **Apenas na Homepage**: O logo header aparece apenas na página inicial (`/`)
✅ **Scroll Inteligente**: Desaparece suavemente ao rolar para baixo, reaparece ao rolar para cima
✅ **Design Profissional**: Gradiente visual atraente e moderno (roxo/azul)
✅ **Responsivo**: Adapta-se perfeitamente em mobile, tablet e desktop
✅ **Acessível**: Respeita configurações de `prefers-reduced-motion`
✅ **Otimizado**: Usa `requestAnimationFrame` e `passive: true` para melhor performance

## Estrutura de Arquivos

```
├── templates/portal/components/logo_header.html    # Template HTML do header
├── static/css/logo-header.css                      # Estilos CSS
└── static/js/logo-header.js                        # Lógica JavaScript
```

## Template HTML

### Arquivo: `templates/portal/components/logo_header.html`

```html
<header id="logo-header" class="logo-header">
    <div class="logo-container">
        <div class="logo-content">
            <img src="..." alt="Logo" class="logo-img">
            <div class="company-info">
                <h1 class="company-name">Seu Portal de Notícias</h1>
                <p class="company-tagline">Notícias atualizadas todos os dias</p>
            </div>
        </div>
    </div>
</header>
```

**Customização:**
- Altere a URL da imagem em `src="..."`
- Atualize `class="company-name"` com o nome da empresa
- Modifique `class="company-tagline"` com o slogan

## Estilos CSS

### Arquivo: `static/css/logo-header.css`

**Cores:**
- Gradiente: `#667eea` → `#764ba2` (roxo/azul)
- Texto: Branco

**Dimensões:**
- Desktop: 70px altura, logo 52px × 52px
- Tablet: 65px altura, logo 48px × 48px
- Mobile: 55px altura, logo 40-44px × 40-44px

**Propriedades principais:**
```css
.logo-header {
    position: fixed;          /* Fixado no topo */
    z-index: 998;             /* Abaixo da navbar */
    transition: transform 0.35s; /* Transição suave */
}

.logo-header.hide {
    transform: translateY(-100%); /* Esconde ao rolar */
}
```

**Responsividade:**
- `@media (max-width: 992px)` - Tablets
- `@media (max-width: 768px)` - Móveis médios
- `@media (max-width: 480px)` - Móveis pequenos
- `@media (prefers-reduced-motion: reduce)` - Acessibilidade

## JavaScript

### Arquivo: `static/js/logo-header.js`

**Funcionalidades:**

1. **Detecção de Página**: Verifica se está na homepage
   - Procura classe `page-home` no body
   - Verifica URLs: `/` ou `/portal/`
   - Suporta múltiplas detecções

2. **Scroll Handler**: Controla visibilidade
   - Limiar: 80px de scroll
   - Detecta direção do scroll
   - Usa `requestAnimationFrame` para otimização

3. **Classes CSS**:
   - Adiciona `page-home` ao body
   - Adiciona `hide` ao logo header quando deve esconder

**Configuração:**
```javascript
const CONFIG = {
    scrollThreshold: 80,  // pixels para começar a esconder
    debounceDelay: 10     // ms para debounce
};
```

## Integração na Homepage

### Arquivo: `templates/portal/home.html`

```django
{% extends 'portal/base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/logo-header.css' %}">
{% endblock %}

{% block content %}
<!-- Logo Header -->
{% include 'portal/components/logo_header.html' %}
<!-- ... resto do conteúdo ... -->
{% endblock %}

<script>
    document.addEventListener('DOMContentLoaded', function() {
        document.body.classList.add('page-home');
    });
</script>
<script src="{% static 'js/logo-header.js' %}"></script>
```

## Comportamento ao Rolar

### Estado 1: Página Carregada (scroll = 0px)
- Logo header **visível**
- Posição fixa no topo
- Navbar abaixo do header

### Estado 2: Rolando para Baixo (scroll > 80px)
- Logo header **desaparece** suavemente
- Navbar assume o topo
- Transição: 0.35s com animação suave

### Estado 3: Rolando para Cima
- Logo header **reaparece** suavemente
- Volta à posição original
- Transição: 0.35s com animação suave

## Customização

### Alterar Cores

**arquivo: `static/css/logo-header.css`**

```css
.logo-header {
    background: linear-gradient(135deg, #SEU_COR_1 0%, #SEU_COR_2 100%);
}
```

Exemplos de gradientes:
- **Azul profissional**: `#2c3e50` → `#3498db`
- **Verde moderno**: `#16a085` → `#1abc9c`
- **Laranja energético**: `#e67e22` → `#e74c3c`

### Alterar Tamanho

```css
.logo-header {
    padding: 20px 0; /* Aumentar/diminuir padding */
}

.logo-img {
    width: 60px;  /* Aumentar/diminuir logo */
    height: 60px;
}

.company-name {
    font-size: 1.5rem; /* Aumentar/diminuir texto */
}
```

### Alterar Limiar de Scroll

**arquivo: `static/js/logo-header.js`**

```javascript
const CONFIG = {
    scrollThreshold: 120, // Aumentar para esconder mais tarde
};
```

### Adicionar a Outras Páginas

Se quiser o logo header em outras páginas, adicione a detecção no JavaScript:

```javascript
// No arquivo logo-header.js, função isOnHomepage()
function isOnHomepage() {
    const path = window.location.pathname;
    // Adicione rotas desejadas
    return path === '/' || path === '/portal/' || path === '/blog/';
}
```

## Performance

- ✅ Usa `requestAnimationFrame` para otimização
- ✅ Listeners com `passive: true`
- ✅ `will-change` em CSS para aceleração de hardware
- ✅ Classe-based IIFE para melhor gerenciamento de memória
- ✅ Detecta e respeita `prefers-reduced-motion`

## Acessibilidade

- ✅ Respeita preferências de movimento reduzido
- ✅ Header semântico com `<header id="logo-header">`
- ✅ Imagem com `alt` text descritivo
- ✅ Headings semânticos (`<h1>`)

## Testes

### Desktop
```bash
1. Abra https://seu-portal.com/
2. Veja o logo header no topo
3. Role para baixo lentamente - deve desaparecer após ~80px
4. Role para cima - deve reaparecer suavemente
5. Volte ao topo - sempre visível
```

### Mobile
```bash
1. Teste em iPhone, Android
2. Verifique responsividade (altura reduzida)
3. Teste scroll em touch
4. Verifique em landscape/portrait
```

### Outras Páginas
```bash
1. Visite /temas/
2. Visite /detalhe/noticia/
3. Verifique que logo header NÃO aparece
```

## Troubleshooting

### Logo header não aparece
- Verifique se `templates/portal/components/logo_header.html` existe
- Verifique se CSS e JS estão sendo carregados (F12 → Network)
- Verifique erros no console (F12 → Console)

### Logo header não desaparece ao rolar
- Verifique se JavaScript está sendo carregado
- Verifique se `page-home` está sendo adicionado ao body
- Aumente `scrollThreshold` se necessário

### Estilos não aplicados
- Limpe cache do navegador (Ctrl+Shift+Delete)
- Verifique se `{% load static %}` está no template
- Verifique se CSS está em `{% block extra_css %}`

### Navbar fica por trás do header
- Verifique z-index do navbar
- Logo header tem `z-index: 998`, navbar deve ter `z-index: 997`

## Commits Relacionados

```
1d517b8 Feature: Add logo header to homepage with scroll behavior
887b301 Improve: Refine logo header styling and scroll behavior
```

## Referências

- [CSS Gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/gradient)
- [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)

---

**Última atualização:** Dezembro 2024
**Versão:** 1.0
