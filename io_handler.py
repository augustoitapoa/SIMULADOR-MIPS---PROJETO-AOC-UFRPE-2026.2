#ENTRADA E SAÍDA DO JSON
import json

class GerenciadorIO:
    @staticmethod
    def carregar_entrada(caminho_arquivo: str) -> list:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, dict):
            # formatado para leitura do código provido pela profa
            return dados.get("text", [])
        elif isinstance(dados, list):
            # lista direta
            return dados
        return []

    @staticmethod
    def salvar_saida(caminho_arquivo: str, dados: list):
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2)