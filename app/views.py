# app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
import json
import re
from collections import Counter

# --- Páginas principais ---
def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def casosbase(request):
    return render(request, 'casosbase.html')

def forum(request):
    return render(request, 'forum.html')

def investigar(request):
    return render(request, 'investigar.html')

def login_view(request):
    return render(request, 'login.html')

# --- Sistema de arquivo JSON (substitui banco temporariamente) ---
INVESTIGACOES_DATA = 'investigacoes_data.json'

def carregar_investigacoes():
    try:
        with open(INVESTIGACOES_DATA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        investigacoes_iniciais = [
            {
                'id': 1,
                'titulo': 'Operação Canteiro - Desvio de Verbas',
                'responsavel': 'Agente Silva',
                'data_inicio': '2025-01-15',
                'data_fim': '2025-03-20',
                'status': 'Concluída',
                'descricao': 'Investigação sobre desvio de verbas públicas em obras do governo municipal. Foram identificados superfaturamento e direcionamento de licitações.',
                'localizacao': 'São Paulo',
                'categoria': 'Corrupção'
            },
            {
                'id': 2,
                'titulo': 'Caso Mai - Tráfico Internacional',
                'responsavel': 'Agente Souza',
                'data_inicio': '2025-04-01',
                'data_fim': None,
                'status': 'Em andamento',
                'descricao': 'Investigação sobre tráfico internacional de drogas envolvendo rotas marítimas. Em fase de coleta de inteligência.',
                'localizacao': 'Rio de Janeiro',
                'categoria': 'Tráfico'
            },
            {
                'id': 3,
                'titulo': 'Operação Farol - Corrupção Federal',
                'responsavel': 'Agente Costa',
                'data_inicio': '2025-02-10',
                'data_fim': '2025-05-30',
                'status': 'Concluída',
                'descricao': 'Investigação de corrupção em órgãos públicos federais. Resultou em 15 prisões e recuperação de R$ 50 milhões.',
                'localizacao': 'Brasília',
                'categoria': 'Corrupção'
            },
        ]
        salvar_investigacoes(investigacoes_iniciais)
        return investigacoes_iniciais

def salvar_investigacoes(investigacoes):
    with open(INVESTIGACOES_DATA, 'w', encoding='utf-8') as f:
        json.dump(investigacoes, f, ensure_ascii=False, indent=2)

def get_proximo_id():
    investigacoes = carregar_investigacoes()
    if not investigacoes:
        return 1
    return max(inv['id'] for inv in investigacoes) + 1

def get_investigacao_by_id(id):
    investigacoes = carregar_investigacoes()
    for inv in investigacoes:
        if inv['id'] == id:
            return inv
    return None

# --- Sistema de Relacionamento Automático ---
def extrair_palavras_chave(texto):
    """Extrai palavras-chave de um texto"""
    if not texto:
        return []
    
    texto_limpo = re.sub(r'[^\w\s]', ' ', texto.lower())
    palavras = texto_limpo.split()
    
    stop_words = {
        'a', 'o', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'por', 'como',
        'mais', 'mas', 'foi', 'são', 'ser', 'está', 'que', 'não', 'sim', 'os',
        'as', 'um', 'uma', 'uns', 'umas', 'é', 'se', 'ao', 'pelo', 'pela',
        'nos', 'nas', 'dos', 'das', 'num', 'numa', 'nuns', 'numas', 'esse',
        'essa', 'isso', 'aquele', 'aquela', 'aquilo', 'este', 'esta', 'isto'
    }
    
    palavras_filtradas = [p for p in palavras if len(p) > 3 and p not in stop_words]
    contador = Counter(palavras_filtradas)
    return [palavra for palavra, count in contador.most_common(10)]

def encontrar_investigacoes_relacionadas(investigacao_atual):
    """Encontra investigações relacionadas automaticamente"""
    todas_investigacoes = carregar_investigacoes()
    relacionadas = []
    
    for investigacao in todas_investigacoes:
        if investigacao['id'] == investigacao_atual['id']:
            continue
            
        pontuacao = 0
        motivos = []
        
        # Similaridade no título
        palavras_titulo_atual = set(investigacao_atual['titulo'].lower().split())
        palavras_titulo_outra = set(investigacao['titulo'].lower().split())
        palavras_comuns_titulo = palavras_titulo_atual.intersection(palavras_titulo_outra)
        
        if len(palavras_comuns_titulo) > 0:
            pontuacao += len(palavras_comuns_titulo) * 2
            motivos.append(f"Títulos similares: {', '.join(palavras_comuns_titulo)}")
        
        # Mesma categoria
        if (investigacao_atual.get('categoria') and investigacao.get('categoria') and 
            investigacao_atual['categoria'] == investigacao['categoria']):
            pontuacao += 3
            motivos.append(f"Mesma categoria: {investigacao_atual['categoria']}")
        
        # Mesma localização
        if (investigacao_atual.get('localizacao') and investigacao.get('localizacao') and 
            investigacao_atual['localizacao'].lower() == investigacao['localizacao'].lower()):
            pontuacao += 2
            motivos.append(f"Mesma localização: {investigacao_atual['localizacao']}")
        
        # Mesmo status
        if investigacao_atual['status'] == investigacao['status']:
            pontuacao += 1
            motivos.append(f"Mesmo status: {investigacao_atual['status']}")
        
        # Similaridade na descrição
        palavras_desc_atual = extrair_palavras_chave(investigacao_atual['descricao'])
        palavras_desc_outra = extrair_palavras_chave(investigacao['descricao'])
        palavras_comuns_desc = set(palavras_desc_atual).intersection(set(palavras_desc_outra))
        
        if len(palavras_comuns_desc) > 2:
            pontuacao += len(palavras_comuns_desc)
            motivos.append(f"Assuntos similares: {', '.join(list(palavras_comuns_desc)[:3])}")
        
        if pontuacao >= 3:
            relacionadas.append({
                'investigacao': investigacao,
                'pontuacao': pontuacao,
                'motivos': motivos
            })
    
    relacionadas.sort(key=lambda x: x['pontuacao'], reverse=True)
    return relacionadas[:4]

# --- Views principais do sistema ---
def investigacoes(request):
    investigacoes_list = carregar_investigacoes()
    context = {'investigacoes': investigacoes_list}
    return render(request, 'investigacoes.html', context)

def nova_investigacao(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        responsavel = request.POST.get('responsavel')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim') or None
        status = request.POST.get('status')
        descricao = request.POST.get('descricao')
        localizacao = request.POST.get('localizacao', '')
        categoria = request.POST.get('categoria', '')
        
        nova_inv = {
            'id': get_proximo_id(),
            'titulo': titulo,
            'responsavel': responsavel,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'status': status,
            'descricao': descricao,
            'localizacao': localizacao,
            'categoria': categoria
        }
        
        investigacoes = carregar_investigacoes()
        investigacoes.append(nova_inv)
        salvar_investigacoes(investigacoes)
        
        return redirect('investigacoes')
    
    return render(request, 'nova_investigacao.html')

def relatorio_investigacao(request, id):
    investigacao = get_investigacao_by_id(id)
    
    if not investigacao:
        raise Http404("Investigação não encontrada")
    
    relacionadas = encontrar_investigacoes_relacionadas(investigacao)
    
    context = {
        'investigacao': investigacao,
        'relacionadas': relacionadas
    }
    return render(request, 'relatorio.html', context)

def relatorio_investigacao_pdf(request, id):
    investigacao = get_investigacao_by_id(id)
    
    if not investigacao:
        raise Http404("Investigação não encontrada")
    
    try:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # Cabeçalho
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, "SISTEMA PFI - RELATÓRIO OFICIAL")
        p.line(50, height - 60, width - 50, height - 60)
        
        # Título
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 90, f"Investigação: {investigacao['titulo']}")
        
        # Informações
        p.setFont("Helvetica", 10)
        y = height - 120
        p.drawString(50, y, f"ID: {investigacao['id']}")
        y -= 20
        p.drawString(50, y, f"Responsável: {investigacao['responsavel']}")
        y -= 20
        p.drawString(50, y, f"Data de Início: {investigacao['data_inicio']}")
        y -= 20
        if investigacao['data_fim']:
            p.drawString(50, y, f"Data de Conclusão: {investigacao['data_fim']}")
            y -= 20
        p.drawString(50, y, f"Status: {investigacao['status']}")
        y -= 20
        if investigacao.get('localizacao'):
            p.drawString(50, y, f"Localização: {investigacao['localizacao']}")
            y -= 20
        if investigacao.get('categoria'):
            p.drawString(50, y, f"Categoria: {investigacao['categoria']}")
            y -= 30
        
        # Descrição
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Descrição da Investigação:")
        y -= 20
        p.setFont("Helvetica", 10)
        
        descricao = investigacao['descricao']
        linhas = []
        palavras = descricao.split()
        linha_atual = ""
        
        for palavra in palavras:
            if len(linha_atual + " " + palavra) <= 80:
                linha_atual += " " + palavra
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)
        
        for linha in linhas:
            if y < 100:
                p.showPage()
                p.setFont("Helvetica", 10)
                y = height - 50
            p.drawString(50, y, linha.strip())
            y -= 15
        
        # Rodapé
        p.setFont("Helvetica-Oblique", 8)
        p.drawString(50, 30, "Documento confidencial - Sistema PFI")
        p.drawString(width - 150, 30, "Página 1")
        
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        filename = f"relatorio_{investigacao['titulo'].replace(' ', '_')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório - {investigacao['titulo']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                @media print {{ body {{ margin: 0; padding: 15px; }} .no-print {{ display: none; }} }}
                .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
                .info {{ margin: 15px 0; }}
                .label {{ font-weight: bold; color: #333; }}
                .footer {{ margin-top: 50px; font-size: 0.8em; color: #666; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>SISTEMA PFI - RELATÓRIO OFICIAL</h1>
                <h2>{investigacao['titulo']}</h2>
            </div>
            
            <div class="info">
                <p><span class="label">ID:</span> {investigacao['id']}</p>
                <p><span class="label">Responsável:</span> {investigacao['responsavel']}</p>
                <p><span class="label">Data de Início:</span> {investigacao['data_inicio']}</p>
                <p><span class="label">Status:</span> {investigacao['status']}</p>
                {f'<p><span class="label">Data de Conclusão:</span> {investigacao["data_fim"]}</p>' if investigacao['data_fim'] else ''}
                {f'<p><span class="label">Localização:</span> {investigacao["localizacao"]}</p>' if investigacao.get('localizacao') else ''}
                {f'<p><span class="label">Categoria:</span> {investigacao["categoria"]}</p>' if investigacao.get('categoria') else ''}
            </div>
            
            <div class="info">
                <p class="label">Descrição da Investigação:</p>
                <p>{investigacao['descricao']}</p>
            </div>
            
            <div class="no-print" style="margin-top: 30px; padding: 15px; background: #f5f5f5;">
                <p><strong>Instruções para salvar como PDF:</strong></p>
                <ol>
                    <li>Pressione <kbd>Ctrl+P</kbd></li>
                    <li>Selecione "Salvar como PDF" como impressora</li>
                    <li>Clique em "Salvar"</li>
                </ol>
                <a href="/investigacoes/">← Voltar à lista</a>
            </div>
            
            <div class="footer">
                Documento confidencial - Sistema PFI
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content)