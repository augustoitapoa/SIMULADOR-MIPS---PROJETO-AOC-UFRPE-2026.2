# decodificação das instruções MIPS em 32 bits (hexadecimal para assembly)


class DecodificadorInstrucoes:
    # Funções para instruções tipo R opcode = 0x00
    R_FUNCT_MAP = {
        0x20: ("add", "R_3OP"),
        0x21: ("addu", "R_3OP"),
        0x22: ("sub", "R_3OP"),
        0x23: ("subu", "R_3OP"),
        0x24: ("and", "R_3OP"),
        0x25: ("or", "R_3OP"),
        0x26: ("xor", "R_3OP"),
        0x27: ("nor", "R_3OP"),
        0x2a: ("slt", "R_3OP"),
        0x2b: ("sltu", "R_3OP"),
        0x00: ("sll", "R_SHIFT"),
        0x02: ("srl", "R_SHIFT"),
        0x03: ("sra", "R_SHIFT"),
        0x04: ("sllv", "R_SHIFT_V"),
        0x06: ("srlv", "R_SHIFT_V"),
        0x07: ("srav", "R_SHIFT_V"),
        0x08: ("jr", "R_JR"),
        0x09: ("jalr", "R_JALR"),
        0x10: ("mfhi", "R_1OP_RD"),
        0x11: ("mthi", "R_1OP_RS"),
        0x12: ("mflo", "R_1OP_RD"),
        0x13: ("mtlo", "R_1OP_RS"),
        0x18: ("mult", "R_2OP"),
        0x19: ("multu", "R_2OP"),
        0x1a: ("div", "R_2OP"),
        0x1b: ("divu", "R_2OP"),
        0x0c: ("syscall", "R_SYSCALL")
    }

    # Mapeamento para instruções tipo-I e tipo-J
    OPCODE_MAP = {
        0x08: ("addi", "I_ALU"),
        0x09: ("addiu", "I_ALU"),
        0x0c: ("andi", "I_LOGIC"),
        0x0d: ("ori", "I_LOGIC"),
        0x0e: ("xori", "I_LOGIC"),
        0x0f: ("lui", "I_LUI"),
        0x0a: ("slti", "I_ALU"),
        0x0b: ("sltiu", "I_ALU"),
        0x04: ("beq", "I_BRANCH"),
        0x05: ("bne", "I_BRANCH"),
        0x06: ("blez", "I_BRANCH_Z"),
        0x07: ("bgtz", "I_BRANCH_Z"),
        0x20: ("lb", "I_MEM"),
        0x21: ("lh", "I_MEM"),
        0x23: ("lw", "I_MEM"),
        0x24: ("lbu", "I_MEM"),
        0x25: ("lhu", "I_MEM"),
        0x28: ("sb", "I_MEM"),
        0x29: ("sh", "I_MEM"),
        0x2b: ("sw", "I_MEM"),
        0x02: ("j", "J_TYPE"),
        0x03: ("jal", "J_TYPE")
    }

    @staticmethod
    def _to_signed_16(val: int) -> int:
        #conversão valor imediato de 16 bits (não sinalizado p/ sinalizado)
        return val if val < 0x8000 else val - 0x10000

    @classmethod
    def decodificar(cls, hex_str: str) -> dict:
        #decodificando a instrução em hexa na estrutura correta
        clean_hex = hex_str.strip()
        val = int(clean_hex, 16)

        opcode = (val >> 26) & 0x3F
        rs = (val >> 21) & 0x1F
        rt = (val >> 16) & 0x1F
        rd = (val >> 11) & 0x1F
        shamt = (val >> 6) & 0x1F
        funct = val & 0x3F
        imm_raw = val & 0xFFFF
        imm_signed = cls._to_signed_16(imm_raw)
        address = val & 0x03FFFFFF

        parsed = {
            "hex": clean_hex,
            "val": val,
            "opcode": opcode,
            "rs": rs,
            "rt": rt,
            "rd": rd,
            "shamt": shamt,
            "funct": funct,
            "imm_raw": imm_raw,
            "imm_signed": imm_signed,
            "address": address,
            "mnemonic": "unknown",
            "text": "unknown",
            "category": "UNKNOWN"
        }

        # Decodificação de Tipo R (Opcode 0x00)
        if opcode == 0x00:
            if funct in cls.R_FUNCT_MAP:
                mnemonic, fmt = cls.R_FUNCT_MAP[funct]
                parsed["mnemonic"] = mnemonic
                parsed["category"] = fmt

                if fmt == "R_3OP":
                    parsed["text"] = f"{mnemonic} ${rd}, ${rs}, ${rt}"
                elif fmt == "R_SHIFT":
                    parsed["text"] = f"{mnemonic} ${rd}, ${rt}, {shamt}"
                elif fmt == "R_SHIFT_V":
                    parsed["text"] = f"{mnemonic} ${rd}, ${rt}, ${rs}"
                elif fmt == "R_2OP":
                    parsed["text"] = f"{mnemonic} ${rs}, ${rt}"
                elif fmt == "R_1OP_RD":
                    parsed["text"] = f"{mnemonic} ${rd}"
                elif fmt == "R_1OP_RS":
                    parsed["text"] = f"{mnemonic} ${rs}"
                elif fmt == "R_JR":
                    parsed["text"] = f"{mnemonic} ${rs}"
                elif fmt == "R_JALR":
                    parsed["text"] = f"{mnemonic} ${rd}, ${rs}" if rd != 31 else f"{mnemonic} ${rs}"
                elif fmt == "R_SYSCALL":
                    parsed["text"] = "syscall"

        # Decodificação de Tipos I e J
        elif opcode in cls.OPCODE_MAP:
            mnemonic, fmt = cls.OPCODE_MAP[opcode]
            parsed["mnemonic"] = mnemonic
            parsed["category"] = fmt

            if fmt in ("I_ALU", "I_LOGIC"):
                parsed["text"] = f"{mnemonic} ${rt}, ${rs}, {imm_signed if fmt == 'I_ALU' else imm_raw}"
            elif fmt == "I_LUI":
                parsed["text"] = f"{mnemonic} ${rt}, {imm_raw}"
            elif fmt == "I_BRANCH":
                parsed["text"] = f"{mnemonic} ${rs}, ${rt}, {imm_signed}"
            elif fmt == "I_BRANCH_Z":
                parsed["text"] = f"{mnemonic} ${rs}, {imm_signed}"
            elif fmt == "I_MEM":
                parsed["text"] = f"{mnemonic} ${rt}, {imm_signed}(${rs})"
            elif fmt == "J_TYPE":
                parsed["text"] = f"{mnemonic} {address}"

        return parsed