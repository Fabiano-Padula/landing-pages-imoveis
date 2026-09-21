import json
import os
import re

def render_galeria(fotos):
    """Gera o HTML para a galeria de fotos com efeito Lightbox em alta definição."""
    html_items = []
    for index, foto in enumerate(fotos):
        # A primeira foto ocupa um destaque maior no grid
        col_span = "md:col-span-2 md:row-span-2" if index == 0 else ""
        item = f'''
        <a href="{foto['url_full']}" class="glightbox group relative overflow-hidden rounded-2xl block h-64 md:h-full {col_span}" data-gallery="imovel-gallery">
            <img src="{foto['url_thumb']}" alt="{foto.get('legenda', 'Foto do imóvel')}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" loading="lazy">
            <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <span class="text-xs uppercase tracking-widest text-gold bg-black/80 px-4 py-2 rounded-full border border-gold/30">Ampliar Foto</span>
            </div>
        </a>
        '''
        html_items.append(item)
    return "\n".join(html_items)

def render_diferenciais(diferenciais):
    """Gera o HTML para os cards de diferenciais técnicos do imóvel."""
    html_items = []
    for item in diferenciais:
        card = f'''
        <div class="p-6 rounded-2xl glass-panel space-y-2">
            <div class="w-8 h-8 rounded-full bg-gold/10 text-gold flex items-center justify-center font-bold text-xs">✓</div>
            <h4 class="text-white font-medium text-lg">{item['titulo']}</h4>
            <p class="text-zinc-400 text-sm">{item['descricao']}</p>
        </div>
        '''
        html_items.append(card)
    return "\n".join(html_items)

def gerador_landing_page(json_path, template_path, output_dir):
    """Carrega dados e gera o arquivo HTML final compilado."""
    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Preenchimento das tags simples
    replacements = {
        "{{TITULO_IMOVEL}}": dados.get("titulo", ""),
        "{{TITULO_IMOVEL_URL}}": re.sub(r'\s+', '%20', dados.get("titulo", "")),
        "{{SUBTITULO_IMOVEL}}": dados.get("subtitulo", ""),
        "{{CATEGORIA_IMOVEL}}": dados.get("categoria", "Mansão"),
        "{{LOCALIZACAO_CURTA}}": dados.get("localizacao_curta", ""),
        "{{FOTO_HERO}}": dados.get("foto_hero", ""),
        "{{METRAGEM}}": str(dados.get("metragem", "0")),
        "{{SUITES}}": str(dados.get("suites", "0")),
        "{{VAGAS}}": str(dados.get("vagas", "0")),
        "{{VALOR}}": dados.get("valor", "Consulte"),
        "{{DESCRICAO_DETALHADA}}": dados.get("descricao_detalhada", ""),
        "{{NOME_CORRETOR}}": dados.get("corretor", {}).get("nome", ""),
        "{{CARGO_CORRETOR}}": dados.get("corretor", {}).get("cargo", "Consultor Imobiliário VIP"),
        "{{FOTO_CORRETOR}}": dados.get("corretor", {}).get("foto", ""),
        "{{WHATSAPP_NUMERO}}": dados.get("corretor", {}).get("whatsapp", ""),
        "{{GALERIA_HTML}}": render_galeria(dados.get("fotos", [])),
        "{{DIFERENCIAIS_HTML}}": render_diferenciais(dados.get("diferenciais", []))
    }

    html_final = template
    for key, value in replacements.items():
        html_final = html_final.replace(key, value)

    # Cria diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    slug_imovel = dados.get("slug", "imovel-luxo")
    path_saida = os.path.join(output_dir, f"{slug_imovel}.html")

    with open(path_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)

    print(f"Landing page criada com sucesso em: {path_saida}")

if __name__ == "__main__":
    gerador_landing_page(
        json_path="imovel_exemplo.json",
        template_path="templates/index.html",  # <-- Adicione "templates/" aqui!
        output_dir="public"                     # <-- Altere para "public" para já salvar na pasta certa da Vercel
    )