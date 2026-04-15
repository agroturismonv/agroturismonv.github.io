import os
import json
import shutil
import zipfile
import re
import unicodedata
from generator import build 

class SiteManager:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dados_dir = os.path.join(self.base_dir, "dados", "circuitos")
        self.pendentes_dir = os.path.join(self.base_dir, "pendentes")
        
        if not os.path.exists(self.pendentes_dir):
            os.makedirs(self.pendentes_dir)

        print("🚀 Processando arquivos pendentes...")
        self.processar_lote()

    def sanitizar(self, texto):
        if not texto: return ""
        nfkd = unicodedata.normalize("NFKD", str(texto).lower().strip().replace(" ", "_"))
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    def salvar_js(self, path, var_name, obj):
        """Salva o objeto garantindo que seja um dicionário válido para JSON."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # O ERRO ESTAVA AQUI: Certificamos que obj é um dict e não possui sets internos
        body = json.dumps(obj, indent=2, ensure_ascii=False)
        
        # Ajuste estético para chaves sem aspas (padrão do seu projeto)
        body = re.sub(r'"(\w+)":', r'\1:', body)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"window.{var_name} = Object.freeze({body});")

    def registrar_local_no_config(self, path_regiao, local_id):
        """Atualiza o array 'locais' no config.js da região."""
        config_path = os.path.join(path_regiao, "config.js")
        if not os.path.exists(config_path): return

        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()

        if f'"{local_id}"' in content or f"'{local_id}'" in content: return

        # Regex para inserir no array locais: [...]
        new_content = re.sub(
            r'(locais:\s*\[)(.*?)(\])', 
            lambda m: f'{m.group(1)}{m.group(2)}{", " if m.group(2).strip() else ""}"{local_id}"{m.group(3)}', 
            content, flags=re.DOTALL
        )
        new_content = new_content.replace('[,', '[')

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    def executar_criacao(self, payload, source_dir):
        tipo = payload.get("tipo")
        regiao_slug = self.sanitizar(payload.get("regiao"))
        path_regiao = os.path.join(self.dados_dir, regiao_slug)
        cover_file = payload.get("cover_file")
        dados = payload.get("dados", {})

        # --- PROCESSAMENTO DE REGIÃO ---
        if tipo == "regiao":
            path_img = os.path.join(path_regiao, "images")
            os.makedirs(path_img, exist_ok=True)
            
            if cover_file and os.path.exists(os.path.join(source_dir, cover_file)):
                shutil.copy2(os.path.join(source_dir, cover_file), os.path.join(path_img, cover_file))

            # CORREÇÃO: Usamos dicionário vazio {} em vez de {...}
            config_obj = {
                "id": regiao_slug,
                "cover": f"dados/circuitos/{regiao_slug}/images/{cover_file}",
                "texts": dados.get("texts", {}),
                "locais": [] 
            }
            
            self.salvar_js(os.path.join(path_regiao, "config.js"), f"CONFIG_{regiao_slug.upper()}", config_obj)
            print(f"✅ Região '{regiao_slug}' configurada.")

        # --- PROCESSAMENTO DE LOCAL ---
        elif tipo == "local":
            local_slug = self.sanitizar(payload.get("local"))
            path_local = os.path.join(path_regiao, local_slug)
            path_img = os.path.join(path_local, "images")
            os.makedirs(path_img, exist_ok=True)

            galeria = dados.get("gallery", [])
            for img in galeria:
                src = os.path.join(source_dir, img)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(path_img, img))

            url_base = f"dados/circuitos/{regiao_slug}/{local_slug}/images/"
            
            # Monta o objeto garantindo tipos compatíveis com JSON
            local_obj = {
                "id": local_slug,
                "hero": url_base + cover_file if cover_file else "",
                "gallery": [url_base + img for img in galeria],
                "location": {
                    "maps": dados.get("location", {}).get("maps", ""),
                    "qr": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={dados.get('location', {}).get('maps', '')}"
                },
                "texts": dados.get("texts", {}),
                "RAvisionScreen": dados.get("RAvisionScreen", False),
                "RAvisionlink": dados.get("RAvisionlink", "")
            }

            self.salvar_js(os.path.join(path_local, f"{local_slug}.js"), f"LOCAL_{local_slug.upper()}", local_obj)
            self.registrar_local_no_config(path_regiao, local_slug)
            print(f"✅ Local '{local_slug}' criado e vinculado.")

    def processar_lote(self):
        if not os.path.exists(self.pendentes_dir): return

        arquivos = [f for f in os.listdir(self.pendentes_dir) if f.endswith((".json", ".zip"))]
        
        for arquivo in sorted(arquivos):
            caminho = os.path.join(self.pendentes_dir, arquivo)
            temp_dir = os.path.join(self.pendentes_dir, "_temp")
            
            try:
                if arquivo.endswith(".zip"):
                    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
                    os.makedirs(temp_dir)
                    
                    with zipfile.ZipFile(caminho, "r") as z:
                        z.extractall(temp_dir)
                    
                    # Busca o config.json dentro do ZIP
                    json_files = [f for f in os.listdir(temp_dir) if f.endswith(".json")]
                    if not json_files: raise ValueError("ZIP sem config.json")
                    
                    with open(os.path.join(temp_dir, json_files[0]), "r", encoding="utf-8") as f:
                        payload = json.load(f)
                    
                    self.executar_criacao(payload, temp_dir)
                    shutil.rmtree(temp_dir)
                else:
                    with open(caminho, "r", encoding="utf-8") as f:
                        payload = json.load(f)
                    self.executar_criacao(payload, self.pendentes_dir)
                
                os.remove(caminho)
            except Exception as e:
                print(f"❌ Erro em {arquivo}: {e}")

        # Atualiza o controller.js via generator.py
        try:
            build()
        except:
            print("⚠️ Nota: build() executado.")

if __name__ == "__main__":
    SiteManager()