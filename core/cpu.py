
class CPU:
    def __init__(self, registradores):
        self.registradores = registradores
        self.stdout = ""

    def executar(self, instrucao: dict):
        """Executa uma instrução decodificada."""
        mnemonic = instrucao["mnemonic"]
        rs, rt, rd = instrucao["rs"], instrucao["rt"], instrucao["rd"]
        shamt = instrucao["shamt"]
        imm_s = instrucao["imm_signed"]
        imm_u = instrucao["imm_raw"]

        # PC + 4 para caminhar as instruções
        self.registradores.pc += 4

        # --- INSTRUÇÕES TIPO R ---
        if mnemonic == "add" or mnemonic == "addu":
            resultado = (self.registradores.obter_registrador(rs) + self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, resultado)

        elif mnemonic == "sub" or mnemonic == "subu":
            resultado = (self.registradores.obter_registrador(rs) - self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, resultado)

        elif mnemonic == "and":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) & self.registradores.obter_registrador(rt))

        elif mnemonic == "or":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) | self.registradores.obter_registrador(rt))

        elif mnemonic == "xor":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) ^ self.registradores.obter_registrador(rt))

        elif mnemonic == "nor":
            resultado = ~(self.registradores.obter_registrador(rs) | self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, resultado)

        elif mnemonic == "slt":
            valor_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            valor_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, 1 if valor_rs < valor_rt else 0)

        elif mnemonic == "sltu":
            valor_rs = self.registradores.obter_registrador(rs)
            valor_rt = self.registradores.obter_registrador(rt)
            self.registradores.definir_registrador(rd, 1 if valor_rs < valor_rt else 0)

        elif mnemonic == "sll":
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) << shamt) & 0xFFFFFFFF)

        elif mnemonic == "srl":
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) & 0xFFFFFFFF) >> shamt)

        elif mnemonic == "sra":
            valor_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, (valor_rt >> shamt) & 0xFFFFFFFF)

        elif mnemonic == "sllv":
            deslocamento = self.registradores.obter_registrador(rs) & 0x1F
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) << deslocamento) & 0xFFFFFFFF)

        elif mnemonic == "srlv":
            deslocamento = self.registradores.obter_registrador(rs) & 0x1F
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) & 0xFFFFFFFF) >> deslocamento)

        elif mnemonic == "srav":
            deslocamento = self.registradores.obter_registrador(rs) & 0x1F
            valor_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, (valor_rt >> deslocamento) & 0xFFFFFFFF)

        elif mnemonic == "mult":
            valor_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            valor_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            produto = valor_rs * valor_rt
            self.registradores.lo = produto & 0xFFFFFFFF
            self.registradores.hi = (produto >> 32) & 0xFFFFFFFF

        elif mnemonic == "multu":
            valor_rs = self.registradores.obter_registrador(rs)
            valor_rt = self.registradores.obter_registrador(rt)
            produto = valor_rs * valor_rt
            self.registradores.lo = produto & 0xFFFFFFFF
            self.registradores.hi = (produto >> 32) & 0xFFFFFFFF

        elif mnemonic == "div":
            valor_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            valor_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            if valor_rt != 0:
                self.registradores.lo = int(valor_rs / valor_rt) & 0xFFFFFFFF
                self.registradores.hi = (valor_rs % valor_rt) & 0xFFFFFFFF

        elif mnemonic == "divu":
            valor_rs = self.registradores.obter_registrador(rs)
            valor_rt = self.registradores.obter_registrador(rt)
            if valor_rt != 0:
                self.registradores.lo = (valor_rs // valor_rt) & 0xFFFFFFFF
                self.registradores.hi = (valor_rs % valor_rt) & 0xFFFFFFFF

        elif mnemonic == "mfhi":
            self.registradores.definir_registrador(rd, self.registradores.hi)

        elif mnemonic == "mflo":
            self.registradores.definir_registrador(rd, self.registradores.lo)

        elif mnemonic == "mthi":
            self.registradores.hi = self.registradores.obter_registrador(rs)

        elif mnemonic == "mtlo":
            self.registradores.lo = self.registradores.obter_registrador(rs)

        # --- INSTRUÇÕES TIPO I (Aritméticas e Lógicas) ---
        elif mnemonic == "addi" or mnemonic == "addiu":
            resultado = (self.registradores.obter_registrador(rs) + imm_s) & 0xFFFFFFFF
            self.registradores.definir_registrador(rt, resultado)

        elif mnemonic == "andi":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) & imm_u)

        elif mnemonic == "ori":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) | imm_u)

        elif mnemonic == "xori":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) ^ imm_u)

        elif mnemonic == "lui":
            self.registradores.definir_registrador(rt, (imm_u << 16) & 0xFFFFFFFF)

        elif mnemonic == "slti":
            valor_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            self.registradores.definir_registrador(rt, 1 if valor_rs < imm_s else 0)

        elif mnemonic == "sltiu":
            valor_rs = self.registradores.obter_registrador(rs)
            self.registradores.definir_registrador(rt, 1 if valor_rs < (imm_s & 0xFFFFFFFF) else 0)