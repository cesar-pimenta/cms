from django.core.management.base import BaseCommand
from portal.models import Tema, Editorial
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Carrega dados de exemplo para o portal'

    def handle(self, *args, **options):
        # Criar temas
        temas_data = [
            {
                'nome': 'Tecnologia',
                'slug': 'tecnologia',
                'descricao': 'Notícias sobre tecnologia e inovação'
            },
            {
                'nome': 'Saúde',
                'slug': 'saude',
                'descricao': 'Notícias sobre saúde e bem-estar'
            },
            {
                'nome': 'Economia',
                'slug': 'economia',
                'descricao': 'Notícias sobre economia e negócios'
            },
            {
                'nome': 'Esportes',
                'slug': 'esportes',
                'descricao': 'Notícias sobre esportes e eventos'
            },
            {
                'nome': 'Cultura',
                'slug': 'cultura',
                'descricao': 'Notícias sobre cultura e arte'
            },
        ]

        temas_criados = []
        for tema_data in temas_data:
            tema, created = Tema.objects.get_or_create(
                slug=tema_data['slug'],
                defaults={
                    'nome': tema_data['nome'],
                    'descricao': tema_data['descricao'],
                    'ativo': True
                }
            )
            temas_criados.append(tema)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Tema "{tema.nome}" criado com sucesso')
                )
            else:
                self.stdout.write(f'Tema "{tema.nome}" já existe')

        # Criar editoriais de exemplo
        editoriais_data = [
            {
                'titulo': 'Inteligência Artificial revoluciona a indústria',
                'texto': 'A inteligência artificial está transformando como as empresas trabalham. Novas modelos de IA conseguem realizar tarefas complexas que antes eram feitas apenas por humanos. Grandes investimentos estão sendo feitos no setor de tecnologia para desenvolver soluções cada vez mais sofisticadas.',
                'layout': 'layout1',
                'estilo': 1,
                'temas': [temas_criados[0]],  # Tecnologia
            },
            {
                'titulo': 'Novos tratamentos para diabetes',
                'texto': 'Pesquisadores anunciaram novas descobertas no tratamento de diabetes tipo 2. Os testes clínicos mostram resultados promissores com uma taxa de sucesso de 85%. Especialistas indicam que os medicamentos podem estar disponíveis em breve.',
                'layout': 'layout2',
                'estilo': 2,
                'temas': [temas_criados[1]],  # Saúde
            },
            {
                'titulo': 'Mercado em alta com otimismo econômico',
                'texto': 'As bolsas de valores registram uma semana positiva com investidores otimistas com as perspectivas econômicas. O dólar recua e o real ganha força. Analistas apontam que a inflação está sob controle e que há espaço para crescimento econômico.',
                'layout': 'layout3',
                'estilo': 3,
                'temas': [temas_criados[2]],  # Economia
            },
            {
                'titulo': 'Seleção conquista vitória espetacular',
                'texto': 'Em um jogo emocionante, a seleção venceu com um placar de 3 a 1. Os torcedores lotaram o estádio para assistir ao espetáculo. O técnico comemorou a performance da equipe e projetou boas perspectivas para os próximos jogos.',
                'layout': 'layout1',
                'estilo': 1,
                'temas': [temas_criados[3]],  # Esportes
            },
            {
                'titulo': 'Exposição de arte contemporânea atrai multidão',
                'texto': 'A nova exposição de arte contemporânea no museu já atraiu mais de 10 mil visitantes. O curador destaca as obras inovadoras de artistas nacionais e internacionais. A exposição fica aberta até o final do mês.',
                'layout': 'layout2',
                'estilo': 2,
                'temas': [temas_criados[4]],  # Cultura
            },
        ]

        agora = timezone.now()
        for i, editorial_data in enumerate(editoriais_data):
            editorial, created = Editorial.objects.get_or_create(
                titulo=editorial_data['titulo'],
                defaults={
                    'texto': editorial_data['texto'],
                    'layout': editorial_data['layout'],
                    'estilo': editorial_data['estilo'],
                    'status': 'publicado',
                    'ativo': True,
                    'data_publicacao': agora - timedelta(days=i),
                    'visualizacoes': 10 + (i * 5),
                }
            )
            
            for tema in editorial_data['temas']:
                editorial.temas.add(tema)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Editorial "{editorial.titulo}" criado com sucesso')
                )
            else:
                self.stdout.write(f'Editorial "{editorial.titulo}" já existe')

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo carregados com sucesso!')
        )
