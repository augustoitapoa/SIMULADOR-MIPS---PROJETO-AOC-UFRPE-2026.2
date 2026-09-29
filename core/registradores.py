#Gerenciador do Banco de Registradores do processador.

class BancoRegistradores:
    def __init__(self, pc_inicial: int = 0):
        # 32 registradores de propósito geral
        self.regs = [0] * 32
        self.pc = pc_inicial
        self.hi = 0
        self.lo = 0

    def obter_registrador(self, indice: int) -> int:
        #leitor do registrador $0 = 0 sempre como no MIPS
        if indice == 0:
            return 0
        return self.regs[indice]

    def definir_registrador(self, indice: int, valor: int):
        #define um valor em 32 bits no registrador ($0 não deve ser alterado como funcionamento normal do MIPS)
        if indice != 0:
            self.regs[indice] = valor & 0xFFFFFFFF

    def obter_dicionario_nao_zero(self) -> dict:
        #retorna registradores != 0
        resultado = {}
        for i in range(32):
            if self.regs[i] != 0:
                resultado[f"${i}"] = self._para_com_sinal_32(self.regs[i])

        if self.pc != 0:
            resultado["pc"] = self.pc
        if self.hi != 0:
            resultado["hi"] = self._para_com_sinal_32(self.hi)
        if self.lo != 0:
            resultado["lo"] = self._para_com_sinal_32(self.lo)

        return resultado

    @staticmethod
    def _para_com_sinal_32(valor: int) -> int:
        #Não sinalizado para sinalizado
        valor = valor & 0xFFFFFFFF
        return valor if valor < 0x80000000 else valor - 0x100000000