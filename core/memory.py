class Memoria:
    def __init__(self):
        self.dados = {}

    def carregar_configuracao(self, config_mem: dict):
        if isinstance(config_mem, dict):
            for end_str, valor in config_mem.items():
                endereco = int(end_str)
                self.escrever_byte(endereco, int(valor))

    def escrever_byte(self, endereco: int, valor: int):
        byte_val = valor & 0xFF
        if byte_val != 0:
            self.dados[endereco] = byte_val
        elif endereco in self.dados:
            del self.dados[endereco]

    def ler_byte(self, endereco: int) -> int:
        return self.dados.get(endereco, 0)

    def ler_byte_com_sinal(self, endereco: int) -> int:
        val = self.ler_byte(endereco)
        return val if val < 0x80 else val - 0x100

    def escrever_meia_palavra(self, endereco: int, valor: int):
        self.escrever_byte(endereco, (valor >> 8) & 0xFF)
        self.escrever_byte(endereco + 1, valor & 0xFF)

    def ler_meia_palavra(self, endereco: int, com_sinal: bool = True) -> int:
        byte_alto = self.ler_byte(endereco)
        byte_baixo = self.ler_byte(endereco + 1)
        val = (byte_alto << 8) | byte_baixo
        if com_sinal and val >= 0x8000:
            return val - 0x10000
        return val

    def escrever_palavra(self, endereco: int, valor: int):
        self.escrever_byte(endereco, (valor >> 24) & 0xFF)
        self.escrever_byte(endereco + 1, (valor >> 16) & 0xFF)
        self.escrever_byte(endereco + 2, (valor >> 8) & 0xFF)
        self.escrever_byte(endereco + 3, valor & 0xFF)

    def ler_palavra(self, endereco: int) -> int:
        b0 = self.ler_byte(endereco)
        b1 = self.ler_byte(endereco + 1)
        b2 = self.ler_byte(endereco + 2)
        b3 = self.ler_byte(endereco + 3)
        return (b0 << 24) | (b1 << 16) | (b2 << 8) | b3

    def obter_dicionario_nao_zero(self) -> dict:
        resultado = {}
        for endereco in sorted(self.dados.keys()):
            val = self.dados[endereco]
            if val != 0:
                resultado[str(endereco)] = val
        return resultado
