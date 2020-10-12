# import datetime
import json


class Inputs:

    """
    Está classe é responsável por receber e tratar os inputs iniciais do user.
    """

    def __init__(self) -> None:
        """
        Esta função é responsável por construir a classe.
        """
        try:
            tema = input("Insira aqui o tema desejado: ")
            self.TEMA_CENTRAL = self.trata_texto(tema)
            nome = input("Insira aqui o seu nome completo: ")
            self.NOME_AUTOR = self.trata_nome(nome)
            instituicao = input(
                "Insira aqui o nome completo da sua instituição de ensino: ")
            self.NOME_INSTITUICAO = self.trata_nome(instituicao)
            data = input(
                "Insira a data da apresentação seguindo o padrão DD-MM-AA: ")
            self.DATA_APRESENTACAO = self.trata_data(data)
            self.save()

        except ValueError:
            print("String inválida")

        except AttributeError:
            print("Insira os dados no padrão solicitado")

        except Exception as e:
            print(f"Ocorreu a exceção {e} durante a execução do construtor")

    def trata_texto(self, texto: str) -> str:
        """
        Limpa uma String e retorna para o usuário.
        """
        if texto:
            return texto.strip().lower()
        raise ValueError("A String está vazia")

    def trata_nome(self, nome: str) -> str:
        """
        Limpa uma String e a formata como um titulo.
        """
        return self.trata_texto(nome).title()

    def trata_data(self, data: str) -> str:
        """
        Formata a data para o padrão brasileiro.
        """
        dia, mes, ano = map(int, data.split('-'))
        # date = datetime.date(day=dia, month=mes, year=ano)
        meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                    9: "Setembro", 10: "Outubro", 11: "Novembro",
                    12: "Dezembro"}
        date = f"{dia} de {meses[mes]} de {ano}"
        return date

    def save(self) -> bool:
        """
        Esta função salva os atributos em um JSON.
        """
        try:
            dados = {
                "temaCentral": self.TEMA_CENTRAL,
                "autor": self.NOME_AUTOR,
                "instituição": self.NOME_INSTITUICAO,
                "dataApresentacao": self.DATA_APRESENTACAO
            }
            with open('Documents\\dadosInput.json', 'w') as outfile:
                json.dump(dados, outfile, indent=2, ensure_ascii=False)
            return True

        except Exception:
            return False


if __name__ == '__main__':
    inputs = Inputs()
    print(f"O tema da apresentação é: {inputs.TEMA_CENTRAL}")
    print(f"O apresentador é: {inputs.NOME_AUTOR}")
    print(f"O nome da instituição é: {inputs.NOME_INSTITUICAO}")
    print(f"O dia da apresentação é: {inputs.DATA_APRESENTACAO}")
