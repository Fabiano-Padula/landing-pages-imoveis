import json
import os
import sys
from jinja2 import Environment, FileSystemLoader

def gerador_landing_page(json_path, template_path, output_dir, filename_override=None):
    if not os.path.exists(json_path):
        print(f"Erro: Ficheiro de dados '{json_path}' não encontrado.")
        return

    # 1. Carregar os dados do imóvel a partir do JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        dados_imovel = json.load(f)
    
    # 2. Configurar o ambiente do Jinja2 para carregar o template HTML
    template_dir = os.path.dirname(template_path)
    template_filename = os.path.basename(template_path)
    
    env = Environment(loader=FileSystemLoader(template_dir if template_dir else '.'))
    template = env.get_template(template_filename)
    
    # 3. Renderizar o HTML com os dados do JSON
    html_renderizado = template.render(imovel=dados_imovel)
    
    # 4. Criar a pasta de saída se ela não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 5. Definir o nome do ficheiro final (index.html ou o slug do imóvel)
    output_filename = filename_override if filename_override else "index.html"
    if not output_filename.endswith(".html"):
        output_filename += ".html"
        
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_renderizado)
        
    print(f"Landing page gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    # Se receber dados via argumentos da linha de comando (GitHub Actions)
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        out_name = sys.argv[2] if len(sys.argv) > 2 else "index.html"
        gerador_landing_page(
            json_path=json_file,
            template_path="templates/index.html",
            output_dir="public",
            filename_override=out_name
        )
    else:
        # Modo de teste local
        gerador_landing_page(
            json_path="imovel_exemplo.json",
            template_path="templates/index.html",
            output_dir="public",
            filename_override="index.html"
        )