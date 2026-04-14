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

        print("🚀 Processando pendentes...")
        self.processar_lote()

    # =========================================================
    # 🧹 UTIL
    # =========================================================
    def sanitizar(self, texto):
        if not texto:
            return ""
        nfkd = unicodedata.normalize(
            "NFKD",
            str(texto).lower().strip().replace(" ", "_")
        )
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    # =========================================================
    # 📦 CONFIG (LER / ESCREVER)
    # =========================================================
    def ler_config(self, path):
        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.search(r'Object\.freeze\(\s*(\{.*\})\s*\)', content, re.DOTALL)

        if not match:
            raise ValueError("config.js inválido")

        js_obj = match.group(1)

        # 🔧 JS → JSON
        js_obj = re.sub(r'//.*', '', js_obj)
        js_obj = js_obj.replace("'", '"')
        js_obj = re.sub(r'(\w+)\s*:', r'"\1":', js_obj)
        js_obj = re.sub(r',\s*([\]}])', r'\1', js_obj)

        return json.loads(js_obj)

    def salvar_config(self, path, regiao, config_obj):
        body = json.dumps(config_obj, indent=2, ensure_ascii=False)
        body = re.sub(r'"(\w+)":', r'\1:', body)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"/**\n * CONFIGURAÇÃO DO CIRCUITO: {regiao.upper()}\n */\n")
            f.write(f"window.CONFIG_{regiao.upper()} = Object.freeze({body});\n")

    def atualizar_config(self, path, regiao, local, dados, tipo):
        # 🌎 REGIÃO → recria tudo
        if tipo == "regiao" or not os.path.exists(path):
            return {
                "id": regiao,
                "cover": dados["hero"],
                "texts": {
                    lang: {
                        "title": d.get("title"),
                        "subtitle": d.get("subtitle", "")
                    }
                    for lang, d in dados["texts"].items()
                },
                "locais": [local]
            }

        # 📍 LOCAL → só adiciona
        config = self.ler_config(path)

        if not config:
            return {
                "id": regiao,
                "locais": [local]
            }

        config.setdefault("locais", [])

        if local not in config["locais"]:
            config["locais"].append(local)

        return config

    # =========================================================
    # 🖼️ IMAGENS
    # =========================================================
    def mover_imagens(self, origem, destino, arquivos):
        os.makedirs(destino, exist_ok=True)

        for nome in arquivos:
            path_origem = os.path.join(origem, nome)
            if os.path.exists(path_origem):
                shutil.copy2(path_origem, os.path.join(destino, nome))

    # =========================================================
    # 🏗️ PROCESSAMENTO PRINCIPAL
    # =========================================================
    def executar_criacao(self, payload, source_dir):
        regiao = self.sanitizar(payload.get("regiao"))
        local = self.sanitizar(payload.get("local"))
        tipo = payload.get("tipo", "local")
        dados = payload.get("dados", {})
        cover_file = payload.get("cover_file")

        if tipo not in ["local", "regiao"]:
            raise ValueError(f"Tipo inválido: {tipo}")

        path_regiao = os.path.join(self.dados_dir, regiao)
        path_local = os.path.join(path_regiao, local)
        path_img = os.path.join(path_local, "images")

        # 📸 IMAGENS
        base_url = f"dados/circuitos/{regiao}/{local}/images/"
        imagens = list(dict.fromkeys(
            ([cover_file] if cover_file else []) + dados.get("gallery", [])
        ))

        self.mover_imagens(source_dir, path_img, imagens)

        # 🔗 URLs finais
        dados["hero"] = base_url + cover_file if cover_file else ""
        dados["gallery"] = [base_url + img for img in dados.get("gallery", [])]
        dados.setdefault("location", {})
        dados["location"]["qr"] = base_url + "qr-code.png"

        # 📦 CONFIG
        config_path = os.path.join(path_regiao, "config.js")

        config_obj = self.atualizar_config(
            config_path, regiao, local, dados, tipo
        )

        self.salvar_config(config_path, regiao, config_obj)

        # 📍 LOCAL.js
        self.salvar_local(path_local, local, dados)

    # =========================================================
    # 📍 LOCAL.JS
    # =========================================================
    def salvar_local(self, path_local, local, dados):
        os.makedirs(path_local, exist_ok=True)

        body = json.dumps(dados, indent=2, ensure_ascii=False)
        body = re.sub(r'"(\w+)":', r'\1:', body)

        header = f"/**\n * LOCAL: {dados['texts']['pt']['title']}\n */\n"

        with open(os.path.join(path_local, f"{local}.js"), "w", encoding="utf-8") as f:
            f.write(header)
            f.write(f"window.LOCAL_{local.upper()} = Object.freeze({body});")

    # =========================================================
    # 📦 ZIP
    # =========================================================
    def processar_zip(self, caminho):
        temp_dir = os.path.join(self.pendentes_dir, "_temp")

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        os.makedirs(temp_dir)

        with zipfile.ZipFile(caminho, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        json_file = next(f for f in os.listdir(temp_dir) if f.endswith(".json"))

        with open(os.path.join(temp_dir, json_file), "r", encoding="utf-8") as f:
            payload = json.load(f)

        self.executar_criacao(payload, temp_dir)
        shutil.rmtree(temp_dir)

    # =========================================================
    # 🔁 LOOP
    # =========================================================
    def processar_lote(self):
        arquivos = [
            f for f in os.listdir(self.pendentes_dir)
            if f.endswith((".json", ".zip"))
        ]

        for arquivo in sorted(arquivos):
            caminho = os.path.join(self.pendentes_dir, arquivo)

            try:
                if arquivo.endswith(".zip"):
                    self.processar_zip(caminho)
                else:
                    with open(caminho, "r", encoding="utf-8") as f:
                        payload = json.load(f)

                    self.executar_criacao(payload, self.pendentes_dir)

                os.remove(caminho)
                print(f"✅ {arquivo} processado")

            except Exception as e:
                print(f"❌ Erro em {arquivo}: {e}")

        build()


if __name__ == "__main__":
    SiteManager()