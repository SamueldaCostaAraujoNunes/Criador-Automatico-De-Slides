import json
import Algorithmia
import pysbd
from secrets import API_KEY_ALGORITHMIA
from watson import Watson


class Texto:
    """
    A classe Texto é responsável por criar, tratar,
    interpretar e separar os textos a respeito do tema central.
    """

    def __init__(self):
        """
        Inicializa a classe Texto
        """
        # Buscar dados de input
        self.dados_input = self.importa_dados()
        self.watson = Watson()
        self.conteudo = self.pesquisa_no_wikipedia()
        self.conteudo_limpo = self.limpa_conteudo()
        self.sentences = self.quebra_em_sentences()
        self.save()

    def importa_dados(self) -> dict:
        """
        Importa os dados de input do usuário
        """
        with open('Documents\\dadosInput.json', 'r') as j:
            json_data = json.load(j)
            return json_data

    def pesquisa_no_wikipedia(self) -> str:
        nome_artigo = self.consulta_o_algoritmia()
        termos = {
            "articleName": nome_artigo,
            "lang": "pt"
        }
        # url = f"https://en.wikipedia.org/wiki/{nome_artigo.replace(' ', '_')}"
        # self.keywords = self.watson.analyze_url(url)["keywords"]
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        result = algo.pipe(termos).result
        return result["content"]

    def consulta_o_algoritmia(self):
        m_input = {
            "search": self.dados_input["temaCentral"],
            "lang": "pt"
        }
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        return algo.pipe(m_input).result[0]

    def limpa_conteudo(self) -> str:
        without_blank_lines = [line.strip()
                               for line in self.conteudo.split("\n")
                               if line.strip() != "" and
                               (not line.startswith("="))]
        texto_limpo = ' '.join(without_blank_lines)
        return texto_limpo

    def quebra_em_sentences(self) -> list:
        seg = pysbd.Segmenter(language="en", clean=False)
        quebrado = seg.segment(self.conteudo_limpo)
        return quebrado

    def save(self):
        lista_de_sentenças = []
        for i in range(self.dados_input["tamanhoSlide"]):
            sentence = self.sentences[i]
            analise = self.watson.analyze_str(sentence)
            keywords = [keyword["text"] for keyword in analise["keywords"]]
            modelo_sentença = {"text": sentence,
                               "keywords": keywords,
                               "images": []}
            lista_de_sentenças.append(modelo_sentença)

        geral = {"sentences": lista_de_sentenças}
        with open('Documents\\dadosSentences.json', 'w',
                  encoding='utf-8') as outfile:
            json.dump(geral, outfile, indent=2,
                      ensure_ascii=False)


if __name__ == '__main__':
    texto = Texto()
