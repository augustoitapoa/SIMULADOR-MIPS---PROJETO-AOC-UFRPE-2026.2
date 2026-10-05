import json

class GerenciadorIO:
    @staticmethod
    def carregar_entrada(caminho_arquivo: str) -> tuple[list, dict]:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        instrucoes = []
        configuracao = {}

        if isinstance(dados, dict):
            instrucoes = dados.get("text", [])
            configuracao = dados.get("config", {})
        elif isinstance(dados, list):
            instrucoes = dados

        return instrucoes, configuracao

    @staticmethod
    def salvar_saida(caminho_arquivo: str, dados: list):
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2)
