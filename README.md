 RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico em Python para calcular orçamentos de locação da R.M Imóveis usando Programação Orientada a Objetos (POO).

Requisitos
- Python 3.9 ou superior
- Nenhuma biblioteca externa é necessária.

Como executar
1. Baixe ou clone este repositório.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python rentsmart.py
```

No Windows, se o comando `python` não funcionar, tente `py rentsmart.py`.

Funcionalidades
- Seleção de apartamento, casa ou estúdio.
- Adicional por segundo quarto em apartamento ou casa.
- Adicional de garagem para casas e apartamentos.
- Pacote de estacionamento para estúdio e cobrança de vagas adicionais.
- Desconto de 5% para apartamento quando o cliente informa não possuir crianças.
- Taxa contratual de R$ 2.000,00, parcelável em até cinco vezes.
- Validação das entradas.
- Resumo detalhado do orçamento.
- Geração de `projecao_rentsmart.csv` com 12 meses de projeção.

Valores
- Apartamento de 1 quarto: R$ 700,00.
- Apartamento de 2 quartos: R$ 700,00 + R$ 200,00.
- Casa de 1 quarto: R$ 900,00.
- Casa de 2 quartos: R$ 900,00 + R$ 250,00.
- Estúdio: R$ 1.200,00.
- Garagem em casa/apartamento: R$ 300,00 por uma vaga.
- Estúdio: pacote inicial de duas vagas por R$ 250,00; cada vaga acima das duas custa mais R$ 60,00.
- Apartamento sem crianças: desconto de 5% sobre o aluguel após adicionais.
- Taxa contratual: R$ 2.000,00, parcelada em 1 a 5 parcelas.

Estrutura de classes
- `Imovel`: classe-base com categoria e aluguel-base.
- `Apartamento`, `Casa`, `Estudio`: especializações que implementam as regras específicas.
- `Orcamento`: guarda os valores calculados e apresenta o resumo.
- `CalculadoraOrcamento`: coleta e valida os dados e coordena o cálculo.

 Arquivos
- `rentsmart.py`: aplicação principal.
- `projecao_rentsmart.csv`: arquivo gerado após o cálculo de um orçamento.

