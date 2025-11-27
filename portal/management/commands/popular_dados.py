from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from portal.models import Tema, Autor, Editorial
from faker import Faker
import random

fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Popula o banco de dados com temas, autores e editoriais'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpa os dados existentes antes de popular'
        )

    def handle(self, *args, **options):
        if options['limpar']:
            Editorial.objects.all().delete()
            Autor.objects.all().delete()
            Tema.objects.all().delete()
            self.stdout.write('Dados limpos.')

        temas = self.criar_temas()
        autores = self.criar_autores()
        self.criar_editoriais(temas, autores)
        self.stdout.write(self.style.SUCCESS('Dados populados com sucesso!'))

    def criar_temas(self):
        nomes_temas = [
            'Tecnologia',
            'Saúde',
            'Educação',
            'Política',
            'Economia',
            'Esportes',
            'Cultura',
            'Meio Ambiente'
        ]

        temas = []
        for nome in nomes_temas:
            tema, criado = Tema.objects.get_or_create(
                nome=nome,
                defaults={
                    'slug': slugify(nome),
                    'descricao': f'Artigos sobre {nome.lower()}',
                    'ativo': True,
                }
            )
            temas.append(tema)

        return temas

    def criar_autores(self):
        autores = []
        for i in range(15):
            nome = fake.name()
            apelido = fake.first_name().lower()
            
            contador = 1
            apelido_original = apelido
            while Autor.objects.filter(apelido=apelido).exists():
                apelido = f"{apelido_original}{contador}"
                contador += 1
            
            autor, criado = Autor.objects.get_or_create(
                apelido=apelido,
                defaults={
                    'nome_completo': nome,
                    'resumo': fake.paragraph(nb_sentences=3),
                    'ativo': True,
                }
            )
            autores.append(autor)

        return autores

    def criar_editoriais(self, temas, autores):
        for i in range(200):
            titulo = fake.sentence(nb_words=8).rstrip('.')
            
            contador = 1
            titulo_original = titulo
            while Editorial.objects.filter(titulo=titulo).exists():
                titulo = f"{titulo_original} ({contador})"
                contador += 1

            autor = random.choice(autores)
            conteudo = '\n\n'.join(fake.paragraphs(nb=random.randint(3, 8)))
            
            editorial = Editorial.objects.create(
                titulo=titulo,
                texto=conteudo,
                autor=autor,
                status='publicado',
                ativo=True,
                layout=random.choice(['layout1', 'layout2', 'layout3']),
                estilo=random.randint(1, 3),
                data_publicacao=timezone.now(),
            )

            temas_selecionados = random.sample(temas, random.randint(2, 5))
            for tema in temas_selecionados:
                editorial.temas.add(tema)
