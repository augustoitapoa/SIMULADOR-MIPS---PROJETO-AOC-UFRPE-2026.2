import argparse
from core.decoder import DecodificadorInstrucoes
from core.registers import BancoRegistradores
from core.memory import Memoria
from core.cpu import CPU
from io_handler import GerenciadorIO

def executar_simulacao(arquivo_entrada: str, arquivo_saida: str, etapa: int):
    instrucoes_hex, configuracao = GerenciadorIO.carregar_entrada(arquivo_entrada)
    dados_saida = []

    registradores = BancoRegistradores(pc_inicial=0)
    memoria = Memoria()

    if configuracao:
        registradores.carregar_configuracao(configuracao.get("regs", {}))
        memoria.carregar_configuracao(configuracao.get("mem", {}))

    cpu = CPU(registradores, memoria)

    for texto_hex in instrucoes_hex:
        instrucao = DecodificadorInstrucoes.decodificar(texto_hex)

        if etapa == 1:
            dados_saida.append({
                "hex": instrucao["hex"],
                "text": instrucao["text"],
                "regs": {},
                "mem": {},
                "stdout": ""
            })

        elif etapa == 2:
            cpu.executar(instrucao)
            
            dados_saida.append({
                "hex": instrucao["hex"],
                "text": instrucao["text"],
                "regs": registradores.obter_dicionario_nao_zero(),
                "mem": {},
                "stdout": cpu.stdout
            })

        elif etapa == 3:
            cpu.executar(instrucao)

            dados_saida.append({
                "hex": instrucao["hex"],
                "text": instrucao["text"],
                "regs": registradores.obter_dicionario_nao_zero(),
                "mem": memoria.obter_dicionario_nao_zero(),
                "stdout": cpu.stdout
            })

    GerenciadorIO.salvar_saida(arquivo_saida, dados_saida)
    print(f"Sucesso! Resultado da Entrega {etapa} salvo em: {arquivo_saida}")

if __name__ == "__main__":
    analisador = argparse.ArgumentParser(description="Simulador MIPS")
    analisador.add_argument("entrada", help="Caminho do arquivo JSON de entrada")
    analisador.add_argument("saida", help="Caminho do arquivo JSON de saída")
    analisador.add_argument("--etapa", type=int, choices=[1, 2, 3], default=3, help="Etapa/Entrega do projeto (1, 2 ou 3)")

    argumentos = analisador.parse_args()
    executar_simulacao(argumentos.entrada, argumentos.saida, argumentos.etapa)
