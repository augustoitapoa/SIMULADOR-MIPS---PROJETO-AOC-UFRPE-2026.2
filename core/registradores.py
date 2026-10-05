class BancoRegistradores:
    def __init__(self, pc_inicial: int = 0):
        self.regs = [0] * 32
        self.pc = pc_inicial
        self.hi = 0
        self.lo = 0

    def carregar_configuracao(self, config_regs: dict):
        if isinstance(config_regs, dict):
            for chave, valor in config_regs.items():
                val_int = int(valor)
                if chave.startswith("$"):
                    reg_idx = int(chave[1:])
                    self.definir_registrador(reg_idx, val_int)
                elif chave.lower() == "pc":
                    self.pc = val_int
                elif chave.lower() == "hi":
                    self.hi = val_int & 0xFFFFFFFF
                elif chave.lower() == "lo":
                    self.lo = val_int & 0xFFFFFFFF

    def obter_registrador(self, indice: int) -> int:
        if indice == 0:
            return 0
        return self.regs[indice]

    def definir_registrador(self, indice: int, valor: int):
        if indice != 0:
            self.regs[indice] = valor & 0xFFFFFFFF

    def obter_dicionario_nao_zero(self) -> dict:
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
        valor = valor & 0xFFFFFFFF
        return valor if valor < 0x80000000 else valor - 0x100000000
