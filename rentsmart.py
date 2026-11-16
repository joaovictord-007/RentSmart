import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class Orcamento:
    categoria: str
    quartos: int
    vagas_garagem: int
    possui_criancas: bool
    aluguel_base: float
    adicional_quartos: float
    adicional_garagem: float
    desconto: float
    aluguel_mensal: float
    taxa_contratual: float
    parcelas_taxa: int

    @property
    def valor_parcela_taxa(self):
        return self.taxa_contratual / self.parcelas_taxa

    @property
    def total_primeiro_mes(self):
        return self.aluguel_mensal + self.valor_parcela_taxa

    def exibir_resumo(self):
        print("\n" + "=" * 48)
        print("                 RENTSMART")
        print("=" * 48)
        print(f"Categoria:                 {self.categoria.title()}")
        if self.categoria != "estudio":
            print(f"Quartos:                   {self.quartos}")
        print(f"Aluguel-base:              R$ {self.aluguel_base:,.2f}")
        print(f"Adicional por quartos:     R$ {self.adicional_quartos:,.2f}")
        print(f"Adicional de garagem:      R$ {self.adicional_garagem:,.2f}")
        print(f"Desconto aplicado:         R$ {self.desconto:,.2f}")
        print("-" * 48)
        print(f"ALUGUEL MENSAL:             R$ {self.aluguel_mensal:,.2f}")
        print(f"Taxa contratual:           R$ {self.taxa_contratual:,.2f}")
        print(f"Parcelamento da taxa:      {self.parcelas_taxa}x de R$ {self.valor_parcela_taxa:,.2f}")
        print(f"Total no primeiro mês:     R$ {self.total_primeiro_mes:,.2f}")
        print("=" * 48)


class Imovel:
    def __init__(self, categoria, aluguel_base):
        self.categoria = categoria
        self.aluguel_base = aluguel_base

    def calcular_adicional_quartos(self, quartos):
        return 0.0

    def calcular_adicional_garagem(self, vagas):
        return 0.0


class Apartamento(Imovel):
    def __init__(self, quartos):
        super().__init__("apartamento", 700.0)
        self.quartos = quartos

    def calcular_adicional_quartos(self, quartos):
        return 200.0 if quartos == 2 else 0.0

    def calcular_adicional_garagem(self, vagas):
        return 300.0 if vagas == 1 else 0.0


class Casa(Imovel):
    def __init__(self, quartos):
        super().__init__("casa", 900.0)
        self.quartos = quartos

    def calcular_adicional_quartos(self, quartos):
        return 250.0 if quartos == 2 else 0.0

    def calcular_adicional_garagem(self, vagas):
        return 300.0 if vagas == 1 else 0.0


class Estudio(Imovel):
    def __init__(self):
        super().__init__("estudio", 1200.0)

    def calcular_adicional_garagem(self, vagas):
        # O pacote inicial de duas vagas custa R$ 250,00.
        # Vagas acima de duas custam R$ 60,00 cada.
        if vagas == 0:
            return 0.0
        if vagas <= 2:
            return 250.0
        return 250.0 + (vagas - 2) * 60.0


class CalculadoraOrcamento:
    TAXA_CONTRATUAL = 2000.0
    DESCONTO_APARTAMENTO_SEM_CRIANCAS = 0.05

    def criar_orcamento(self):
        print("\n=== RentSmart | Novo orçamento ===")
        categoria = self._escolher_opcao(
            "Tipo de imóvel:\n1 - Apartamento\n2 - Casa\n3 - Estúdio\nEscolha: ",
            {"1", "2", "3"}
        )

        quartos = 0
        if categoria in {"1", "2"}:
            quartos = self._escolher_opcao(
                "Quantidade de quartos (1 ou 2): ",
                {"1", "2"}
            )
            quartos = int(quartos)

        if categoria == "1":
            imovel = Apartamento(quartos)
            nome_categoria = "apartamento"
        elif categoria == "2":
            imovel = Casa(quartos)
            nome_categoria = "casa"
        else:
            imovel = Estudio()
            nome_categoria = "estudio"

        if nome_categoria == "estudio":
            vagas = self._escolher_opcao(
                "Quantidade de vagas (0 ou mais): ", None, inteiro_minimo=0
            )
        else:
            vagas = self._escolher_opcao(
                "Deseja uma vaga de garagem? (s/n): ", {"s", "n"}
            )
            vagas = 1 if vagas == "s" else 0

        possui_criancas = True
        if nome_categoria == "apartamento":
            resposta = self._escolher_opcao(
                "Possui crianças? (s/n): ", {"s", "n"}
            )
            possui_criancas = resposta == "s"

        parcelas = int(self._escolher_opcao(
            "Em quantas parcelas deseja pagar a taxa contratual (1 a 5)? ",
            {"1", "2", "3", "4", "5"}
        ))

        adicional_quartos = imovel.calcular_adicional_quartos(quartos)
        adicional_garagem = imovel.calcular_adicional_garagem(vagas)
        subtotal = imovel.aluguel_base + adicional_quartos + adicional_garagem

        desconto = 0.0
        if nome_categoria == "apartamento" and not possui_criancas:
            desconto = subtotal * self.DESCONTO_APARTAMENTO_SEM_CRIANCAS

        aluguel_mensal = subtotal - desconto

        orcamento = Orcamento(
            categoria=nome_categoria,
            quartos=quartos,
            vagas_garagem=vagas,
            possui_criancas=possui_criancas,
            aluguel_base=imovel.aluguel_base,
            adicional_quartos=adicional_quartos,
            adicional_garagem=adicional_garagem,
            desconto=desconto,
            aluguel_mensal=aluguel_mensal,
            taxa_contratual=self.TAXA_CONTRATUAL,
            parcelas_taxa=parcelas
        )
        orcamento.exibir_resumo()
        caminho_csv = gerar_projecao_csv(orcamento)
        print(f"\nProjeção de 12 meses salva em: {caminho_csv.resolve()}")
        return orcamento

    @staticmethod
    def _escolher_opcao(mensagem, opcoes_validas=None, inteiro_minimo=None):
        while True:
            resposta = input(mensagem).strip().lower()
            if opcoes_validas is not None and resposta not in opcoes_validas:
                print("Opção inválida. Tente novamente.")
                continue
            if inteiro_minimo is not None:
                try:
                    valor = int(resposta)
                    if valor < inteiro_minimo:
                        print(f"Informe um número inteiro maior ou igual a {inteiro_minimo}.")
                        continue
                    return str(valor)
                except ValueError:
                    print("Digite um número inteiro válido.")
                    continue
            return resposta


def gerar_projecao_csv(orcamento, nome_arquivo="projecao_rentsmart.csv"):
    """Gera 12 linhas, uma por mês, com aluguel e taxa contratual separados."""
    caminho = Path(nome_arquivo)
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow([
            "Mes", "Aluguel mensal (R$)", "Parcela taxa contratual (R$)",
            "Total previsto no mes (R$)", "Saldo taxa contratual (R$)"
        ])

        saldo_taxa = orcamento.taxa_contratual
        for mes in range(1, 13):
            parcela_taxa = min(orcamento.valor_parcela_taxa, saldo_taxa)
            total_mes = orcamento.aluguel_mensal + parcela_taxa
            saldo_taxa = max(0.0, saldo_taxa - parcela_taxa)
            escritor.writerow([
                mes,
                f"{orcamento.aluguel_mensal:.2f}",
                f"{parcela_taxa:.2f}",
                f"{total_mes:.2f}",
                f"{saldo_taxa:.2f}"
            ])
    return caminho


def main():
    calculadora = CalculadoraOrcamento()
    while True:
        calculadora.criar_orcamento()
        continuar = input("\nDeseja calcular outro orçamento? (s/n): ").strip().lower()
        if continuar != "s":
            print("Obrigado por utilizar o RentSmart!")
            break


if __name__ == "__main__":
    main()
