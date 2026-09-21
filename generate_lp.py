import json
import os
from jinja2 import Environment, FileSystemLoader

def gerador_landing_page(json_path, template_path, output_dir):
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
    
    # 5. Salvar como index.html para carregar diretamente na raiz da Vercel
    output_path = os.path.join(output_dir, "index.html")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_renderizado)
        
    print(f" Landing page gerada com sucesso em: {output_path}")

if __name__ == "__main__":
    gerador_landing_page(
        json_path="imovel_exemplo.json",
        template_path="templates/index.html",
        output_dir="public"
    )