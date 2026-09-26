import json
import os
from jinja2 import Template

def carregar_dados_json(caminho_json):
    if not os.path.exists(caminho_json):
        print(f"Erro: Ficheiro {caminho_json} não encontrado.")
        return None
    
    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Trata se o payload vier embrulhado pelo Make / GitHub Actions
    if "client_payload" in dados:
        dados = dados["client_payload"]
    if "data" in dados:
        dados = dados["data"]
    if "fields" in dados:
        # Se for payload direto da API do Tally
        res = {}
        for field in dados.get("fields", []):
            label = field.get("label")
            value = field.get("value")
            if label:
                res[label] = value
        return res
        
    return dados

def extrair_lista(valor):
    """Auxiliar para converter texto linha por linha em lista"""
    if not valor:
        return []
    if isinstance(valor, list):
        return valor
    return [item.strip() for item in str(valor).split('\n') if item.strip()]

def extrair_fotos(valor):
    """Auxiliar para extrair URLs de imagens"""
    if not valor:
        return []
    if isinstance(valor, list):
        urls = []
        for item in valor:
            if isinstance(item, dict) and 'url' in item:
                urls.append(item['url'])
            elif isinstance(item, str):
                urls.append(item)
        return urls
    return [str(valor)]

def main():
    payload = carregar_dados_json('dados_tally.json')
    if not payload:
        return

    # Mapeamento exato com base no CSV do Tally
    titulo = payload.get("Título do imóvel", "Imóvel Exclusivo")
    local = payload.get("Local", "")
    valor = payload.get("Valor", "")
    condominio = payload.get("Condomínio", "")
    iptu = payload.get("IPTU anual", "")
    
    area_construida = payload.get("Área construída", "")
    area_terreno = payload.get("Área do terreno", "")
    
    desc_imovel = payload.get("Descrição do imóvel", "")
    desc_condominio = payload.get("Descrição do condomínio", "")
    outras_infos = payload.get("Outras informações", "")
    
    caracteristicas_imovel = extrair_lista(payload.get("Características do imóvel - digite um por linha (ex: 3 Dormitórios, 1 Closet, 1 Lavabo)"))
    caracteristicas_condo = extrair_lista(payload.get("Características do condomínio - digite um por linha (ex: Condomínio fechado, Quadra de areia)"))
    
    foto_principal = extrair_fotos(payload.get("Foto principal"))
    foto_capa = foto_principal[0] if foto_principal else ""
    
    galeria = extrair_fotos(payload.get("Galeria de fotos"))

    print(f"A processar imóvel: {titulo}")
    print(f"Total de fotos na galeria: {len(galeria)}")

    # Carregar Template HTML apontando para a pasta 'templates'
    caminho_template = os.path.join('templates', 'index.html')
    if not os.path.exists(caminho_template):
        caminho_template = 'index.html' # Fallback caso o index.html esteja na raiz

    with open(caminho_template, 'r', encoding='utf-8') as f:
        template_html = f.read()

    template = Template(template_html)
    
    html_renderizado = template.render(
        titulo=titulo,
        local=local,
        valor=valor,
        condominio=condominio,
        iptu=iptu,
        area_construida=area_construida,
        area_terreno=area_terreno,
        desc_imovel=desc_imovel,
        desc_condominio=desc_condominio,
        outras_infos=outras_infos,
        caracteristicas_imovel=caracteristicas_imovel,
        caracteristicas_condo=caracteristicas_condo,
        foto_capa=foto_capa,
        galeria=galeria
    )

    # Guardar na pasta public/index.html para a Vercel/GitHub servir
    os.makedirs('public', exist_ok=True)
    with open(os.path.join('public', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_renderizado)
        
    # Guardar também na raiz por garantia
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_renderizado)

    print("Landing Page gerada com sucesso em public/index.html!")

if __name__ == '__main__':
    main()