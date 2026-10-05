class CPU:
    def __init__(self, registradores, memoria=None):
        self.registradores = registradores
        self.memoria = memoria
        self.stdout = ""

    def executar(self, instrucao: dict):
        mnemonic = instrucao["mnemonic"]
        rs, rt, rd = instrucao["rs"], instrucao["rt"], instrucao["rd"]
        shamt = instrucao["shamt"]
        imm_s = instrucao["imm_signed"]
        imm_u = instrucao["imm_raw"]
        address = instrucao["address"]

        pc_atual = self.registradores.pc
        self.registradores.pc += 4

        if mnemonic in ("add", "addu"):
            res = (self.registradores.obter_registrador(rs) + self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, res)

        elif mnemonic in ("sub", "subu"):
            res = (self.registradores.obter_registrador(rs) - self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, res)

        elif mnemonic == "and":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) & self.registradores.obter_registrador(rt))

        elif mnemonic == "or":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) | self.registradores.obter_registrador(rt))

        elif mnemonic == "xor":
            self.registradores.definir_registrador(rd, self.registradores.obter_registrador(rs) ^ self.registradores.obter_registrador(rt))

        elif mnemonic == "nor":
            res = ~(self.registradores.obter_registrador(rs) | self.registradores.obter_registrador(rt)) & 0xFFFFFFFF
            self.registradores.definir_registrador(rd, res)

        elif mnemonic == "slt":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            v_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, 1 if v_rs < v_rt else 0)

        elif mnemonic == "sltu":
            v_rs = self.registradores.obter_registrador(rs)
            v_rt = self.registradores.obter_registrador(rt)
            self.registradores.definir_registrador(rd, 1 if v_rs < v_rt else 0)

        elif mnemonic == "sll":
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) << shamt) & 0xFFFFFFFF)

        elif mnemonic == "srl":
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) & 0xFFFFFFFF) >> shamt)

        elif mnemonic == "sra":
            v_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, (v_rt >> shamt) & 0xFFFFFFFF)

        elif mnemonic == "sllv":
            shift = self.registradores.obter_registrador(rs) & 0x1F
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) << shift) & 0xFFFFFFFF)

        elif mnemonic == "srlv":
            shift = self.registradores.obter_registrador(rs) & 0x1F
            self.registradores.definir_registrador(rd, (self.registradores.obter_registrador(rt) & 0xFFFFFFFF) >> shift)

        elif mnemonic == "srav":
            shift = self.registradores.obter_registrador(rs) & 0x1F
            v_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            self.registradores.definir_registrador(rd, (v_rt >> shift) & 0xFFFFFFFF)

        elif mnemonic == "mult":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            v_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            prod = v_rs * v_rt
            self.registradores.lo = prod & 0xFFFFFFFF
            self.registradores.hi = (prod >> 32) & 0xFFFFFFFF

        elif mnemonic == "multu":
            v_rs = self.registradores.obter_registrador(rs)
            v_rt = self.registradores.obter_registrador(rt)
            prod = v_rs * v_rt
            self.registradores.lo = prod & 0xFFFFFFFF
            self.registradores.hi = (prod >> 32) & 0xFFFFFFFF

        elif mnemonic == "div":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            v_rt = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rt))
            if v_rt != 0:
                self.registradores.lo = int(v_rs / v_rt) & 0xFFFFFFFF
                self.registradores.hi = (v_rs % v_rt) & 0xFFFFFFFF

        elif mnemonic == "divu":
            v_rs = self.registradores.obter_registrador(rs)
            v_rt = self.registradores.obter_registrador(rt)
            if v_rt != 0:
                self.registradores.lo = (v_rs // v_rt) & 0xFFFFFFFF
                self.registradores.hi = (v_rs % v_rt) & 0xFFFFFFFF

        elif mnemonic == "mfhi":
            self.registradores.definir_registrador(rd, self.registradores.hi)

        elif mnemonic == "mflo":
            self.registradores.definir_registrador(rd, self.registradores.lo)

        elif mnemonic == "mthi":
            self.registradores.hi = self.registradores.obter_registrador(rs)

        elif mnemonic == "mtlo":
            self.registradores.lo = self.registradores.obter_registrador(rs)

        elif mnemonic in ("addi", "addiu"):
            res = (self.registradores.obter_registrador(rs) + imm_s) & 0xFFFFFFFF
            self.registradores.definir_registrador(rt, res)

        elif mnemonic == "andi":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) & imm_u)

        elif mnemonic == "ori":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) | imm_u)

        elif mnemonic == "xori":
            self.registradores.definir_registrador(rt, self.registradores.obter_registrador(rs) ^ imm_u)

        elif mnemonic == "lui":
            self.registradores.definir_registrador(rt, (imm_u << 16) & 0xFFFFFFFF)

        elif mnemonic == "slti":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            self.registradores.definir_registrador(rt, 1 if v_rs < imm_s else 0)

        elif mnemonic == "sltiu":
            v_rs = self.registradores.obter_registrador(rs)
            self.registradores.definir_registrador(rt, 1 if v_rs < (imm_s & 0xFFFFFFFF) else 0)

        elif mnemonic == "beq":
            if self.registradores.obter_registrador(rs) == self.registradores.obter_registrador(rt):
                self.registradores.pc += (imm_s << 2)

        elif mnemonic == "bne":
            if self.registradores.obter_registrador(rs) != self.registradores.obter_registrador(rt):
                self.registradores.pc += (imm_s << 2)

        elif mnemonic == "blez":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            if v_rs <= 0:
                self.registradores.pc += (imm_s << 2)

        elif mnemonic == "bgtz":
            v_rs = self.registradores._para_com_sinal_32(self.registradores.obter_registrador(rs))
            if v_rs > 0:
                self.registradores.pc += (imm_s << 2)

        elif mnemonic == "j":
            self.registradores.pc = (self.registradores.pc & 0xF0000000) | (address << 2)

        elif mnemonic == "jal":
            self.registradores.definir_registrador(31, self.registradores.pc)
            self.registradores.pc = (self.registradores.pc & 0xF0000000) | (address << 2)

        elif mnemonic == "jr":
            self.registradores.pc = self.registradores.obter_registrador(rs)

        elif mnemonic == "jalr":
            self.registradores.definir_registrador(rd, self.registradores.pc)
            self.registradores.pc = self.registradores.obter_registrador(rs)

        elif self.memoria is not None:
            end_base = self.registradores.obter_registrador(rs) + imm_s

            if mnemonic == "lb":
                val = self.memoria.ler_byte_com_sinal(end_base)
                self.registradores.definir_registrador(rt, val)

            elif mnemonic == "lbu":
                val = self.memoria.ler_byte(end_base)
                self.registradores.definir_registrador(rt, val)

            elif mnemonic == "lh":
                val = self.memoria.ler_meia_palavra(end_base, com_sinal=True)
                self.registradores.definir_registrador(rt, val)

            elif mnemonic == "lhu":
                val = self.memoria.ler_meia_palavra(end_base, com_sinal=False)
                self.registradores.definir_registrador(rt, val)

            elif mnemonic == "lw":
                val = self.memoria.ler_palavra(end_base)
                self.registradores.definir_registrador(rt, val)

            elif mnemonic == "sb":
                val = self.registradores.obter_registrador(rt)
                self.memoria.escrever_byte(end_base, val)

            elif mnemonic == "sh":
                val = self.registradores.obter_registrador(rt)
                self.memoria.escrever_meia_palavra(end_base, val)

            elif mnemonic == "sw":
                val = self.registradores.obter_registrador(rt)
                self.memoria.escrever_palavra(end_base, val)
