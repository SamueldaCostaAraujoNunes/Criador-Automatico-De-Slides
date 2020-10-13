import json
import Algorithmia
import pysbd
from secrets import API_KEY_ALGORITHMIA
from watson import Watson
from tqdm import tqdm


class Texto:
    """
    A classe Texto é responsável por criar, tratar,
    interpretar e separar os textos a respeito do tema central.
    """

    def __init__(self):
        """
        Inicializa a classe Texto
        """
        pbar = tqdm(desc="Robô de Texto: ", unit="Process", total=6)
        self.dados = self.load()
        pbar.update(1)
        self.watson = Watson()
        pbar.update(1)
        self.conteudo = self.pesquisa_no_wikipedia()
        pbar.update(1)
        self.conteudo_limpo = self.limpa_conteudo()
        pbar.update(1)
        self.sentences = self.quebra_em_sentences()
        pbar.update(1)
        self.save()
        pbar.update(1)
        pbar.close()

    def pesquisa_no_wikipedia(self) -> str:
        """
        Pesquisa o tema principal no wikipedia
        """
        nome_artigo = self.consulta_o_algoritmia()
        termos = {
            "articleName": nome_artigo,
            "lang": "pt"
        }
        # url = "https://en.wikipedia.org/wiki/" \
        #       f"{nome_artigo.replace(' ', '_')}"
        # self.keywords = self.watson.analyze_url(url)["keywords"]
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        result = algo.pipe(termos).result
        return result["content"]

    def consulta_o_algoritmia(self):
        """
        Verifica qual o artigo que melhor
        se encaixa ao tema central
        """
        m_input = {
            "search": self.dados["input"]["temaCentral"],
            "lang": "pt"
        }
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        return algo.pipe(m_input).result[0]

    def limpa_conteudo(self) -> str:
        """
        Sanitiza o conteudo do wikipedia,
        retirando marcações, linhas em branco
        e as tags de MarkDown
        """
        without_blank_lines = [line.strip()
                               for line in self.conteudo.split("\n")
                               if line.strip() != "" and
                               (not line.startswith("="))]
        texto_limpo = ' '.join(without_blank_lines)
        return texto_limpo

    def quebra_em_sentences(self) -> list:
        """
        Divide o conteudo limpo,
        em uma lista de sentenças lógicas.
        """
        seg = pysbd.Segmenter(language="en", clean=False)
        quebrado = seg.segment(self.conteudo_limpo)
        return quebrado

    def save(self):
        """
        Salva o conteudo tratado no documento,
        dadosSentences.json
        """
        lista_de_sentenças = []
        for i in range(self.dados["input"]["tamanhoSlide"]):
            sentence = self.sentences[i]
            analise = self.watson.analyze_str(sentence)
            keywords = [keyword["text"] for keyword in analise["keywords"]]
            modelo_sentença = {"text": sentence,
                               "keywords": keywords,
                               "images": []}
            lista_de_sentenças.append(modelo_sentença)

        geral = {"sentences": lista_de_sentenças, "input": self.dados["input"]}
        with open('Documents\\dados.json', 'w',
                  encoding='utf-8') as outfile:
            json.dump(geral, outfile, indent=2,
                      ensure_ascii=False)

    def load(self) -> dict:
        """
        Importa os dados de input do usuário
        """
        with open('Documents\\dados.json', 'r', encoding='utf-8') as j:
            json_data = json.load(j)
            return json_data

if __name__ == '__main__':
    texto = Texto()
