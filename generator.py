import os
import json

def build():
    # Caminhos baseados na localização do script para evitar erro de 'Pasta não encontrada'
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(caminho_script, "dados", "circuitos")
    output_file = os.path.join(caminho_script, "dados", "controller.js")
    
    # Estrutura que separa Config (Slider) de Pontos (Cards)
    estrutura_total = {}
    
    print("🚀 Mapeando Hierarquia: Configs -> Pontos...")

    # Varredura das pastas de circuitos
    for nome_circuito in os.listdir(base_dir):
        caminho_circuito = os.path.join(base_dir, nome_circuito)
        
        if os.path.isdir(caminho_circuito):
            # Inicializa o objeto do circuito
            estrutura_total[nome_circuito] = {
                "config": f"../dados/circuitos/{nome_circuito}/config.js",
                "pontos": []
            }
            
            # Varre as subpastas em busca dos arquivos de locais (.js)
            for root, dirs, files in os.walk(caminho_circuito):
                for f in files:
                    if f.endswith('.js') and f != 'config.js':
                        nome_id = f.replace('.js', '')
                        # Caminho relativo para o navegador (Saindo de /layout/)
                        rel_path = os.path.relpath(os.path.join(root, f), os.path.join(caminho_script, "dados")).replace("\\", "/")
                        
                        estrutura_total[nome_circuito]["pontos"].append({
                            "id": nome_id,
                            "src": f"../dados/{rel_path}",
                            "var": f"LOCAL_{nome_id.upper()}"
                        })

    # Gerando o JavaScript do Controller
    js_content = f"""
(function () {{
    const ESTRUTURA = {json.dumps(estrutura_total, indent=2)};
    let carregados = 0;
    let total = 0;

    // Conta quantos scripts existem no total para saber quando parar
    Object.values(ESTRUTURA).forEach(c => {{
        total += 1; // O config.js
        total += c.pontos.length; // Os locais
    }});

    function montarSistema() {{
        // 1. Monta o banco de dados de locais (para circuitos.html e local.html)
        window.LOCAIS = {{}};
        // 2. Monta a lista de circuitos para o Slider (index.html)
        window.LISTA_CIRCUITOS = [];

        Object.values(ESTRUTURA).forEach(circuito => {{
            // Busca a variável CONFIG_ gerada pelo config.js
            const nomePasta = Object.keys(ESTRUTURA).find(key => ESTRUTURA[key] === circuito).toUpperCase();
            const varConfig = "CONFIG_" + nomePasta;
            
            if(window[varConfig]) {{
                window.LISTA_CIRCUITOS.push(window[varConfig]);
            }}

            // Associa os locais carregados ao objeto window.LOCAIS
            circuito.pontos.forEach(ponto => {{
                if(window[ponto.var]) {{
                    window.LOCAIS[ponto.id] = window[ponto.var];
                }}
            }});
        }});

        console.log("✅ Sistema Pronto: Index (Slider) e Circuitos conectados.");
        window.dispatchEvent(new Event('locais-ready'));
    }}

    // Carregador Dinâmico
    Object.values(ESTRUTURA).forEach(circuito => {{
        // Carrega o Config.js
        const sConf = document.createElement('script');
        sConf.src = circuito.config;
        sConf.onload = () => {{ if(++carregados === total) montarSistema(); }};
        document.head.appendChild(sConf);

        // Carrega os Locais
        circuito.pontos.forEach(ponto => {{
            const sLoc = document.createElement('script');
            sLoc.src = ponto.src;
            sLoc.onload = () => {{ if(++carregados === total) montarSistema(); }};
            document.head.appendChild(sLoc);
        }});
    }});
}})();
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"✅ Build finalizado! {len(estrutura_total)} circuitos processados.")

if __name__ == "__main__":
    build()