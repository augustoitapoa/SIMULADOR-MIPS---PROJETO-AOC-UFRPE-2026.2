"""
 Simulador MIPS AOC 2026.2

 AUGUSTO ITAPOA
 RENATO NEVES
 VITOR CARDOSO


Uso por entregas, cada entrega é lida como etapa.

  python main.py input.json output.json --etapa 1
  python main.py input.json output.json --etapa 2
"""

import sys
import argparse
from core.decoder import DecodificadorInstrucoes
from core.registradores import BancoRegistradores
from core.cpu import CPU
from io_handler import GerenciadorIO


def executar_simulacao(arquivo_entrada: str, arquivo_saida: str, etapa: int):
    instrucoes_hex = GerenciadorIO.carregar_entrada(arquivo_entrada)
    dados_saida = []

    registradores = BancoRegistradores(pc_inicial=0)
    cpu = CPU(registradores)

    for texto_hex in instrucoes_hex:
        instrucao = DecodificadorInstrucoes.decodificar(texto_hex)

        if etapa == 1:
            # Entrega 1
            dados_saida.append({
                "hex": instrucao["hex"],
                "text": instrucao["text"],
                "regs": {},
                "mem": {},
                "stdout": ""
            })

        elif etapa == 2:
            # Entrega 2
            cpu.executar(instrucao)

            dados_saida.append({
                "hex": instrucao["hex"],
                "text": instrucao["text"],
                "regs": registradores.obter_dicionario_nao_zero(),
                "mem": {},
                "stdout": cpu.stdout
            })

    GerenciadorIO.salvar_saida(arquivo_saida, dados_saida)
    print(f"Sucesso! Resultado da Entrega {etapa} salvo em: {arquivo_saida}")


if __name__ == "__main__":
    analisador = argparse.ArgumentParser(description="Simulador MIPS")
    analisador.add_argument("entrada", help="Caminho do arquivo JSON de entrada")
    analisador.add_argument("saida", help="Caminho do arquivo JSON de saída")
    analisador.add_argument("--etapa", type=int, choices=[1, 2], default=1, help="Etapa/Entrega do projeto (1 ou 2)")

    argumentos = analisador.parse_args()
    executar_simulacao(argumentos.entrada, argumentos.saida, argumentos.etapa)