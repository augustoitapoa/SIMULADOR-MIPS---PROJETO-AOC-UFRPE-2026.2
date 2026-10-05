Projeto Simulador MIPS AOC

Como testar o funcionamento do código?

Crie um arquivo input.json de exemplo com configuração inicial:

JSON
{
  "config": {
    "regs": { "$1": 5 },
    "mem": { "100": 10 }
  },
  "data": {},
  "text": [
    "0x2002000A",
    "0xAC020064",
    "0x8C030064"
  ]
}
Execute o comando para a Entrega 3:

Bash
python main.py input.json output3.json --etapa 3
