import json
import Algorithmia
import pysbd
from secrets import API_KEY_ALGORITHMIA
from watson import Watson
from tqdm import tqdm
from tradutor import traduz


class Texto:
    """
    A classe Texto é responsável por criar, tratar,
    interpretar e separar os textos a respeito do tema central.
    """

    def __init__(self):
        """
        Inicializa a classe Texto
        """
        pbar = tqdm(desc="Robô de Texto: ", total=8)
        self.load()
        pbar.update()
        self.cria_watson()
        pbar.update()
        self.pesquisa_no_wikipedia()
        pbar.update()
        self.limpa_conteudo()
        pbar.update()
        self.quebra_em_sentences()
        pbar.update()
        self.cria_keywords()
        pbar.update()
        self.traduzir_sentences()
        pbar.update()
        self.save()
        pbar.update()
        pbar.close()

    def cria_watson(self):
        self.watson = Watson()

    def pesquisa_no_wikipedia(self):
        """
        Pesquisa o tema principal no wikipedia
        """
        nome_artigo = self.consulta_o_algoritmia()
        termos = {
            "articleName": nome_artigo,
            "lang": "en"
        }
        # url = "https://en.wikipedia.org/wiki/" \
        #       f"{nome_artigo.replace(' ', '_')}"
        # self.keywords = self.watson.analyze_url(url)["keywords"]
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        result = algo.pipe(termos).result
        self.conteudo = result["content"]

    def consulta_o_algoritmia(self):
        """
        Verifica qual o artigo que melhor
        se encaixa ao tema central
        """
        m_input = {
            "search": self.dados["input"]["temaCentral"],
            "lang": "en"
        }
        client = Algorithmia.client(API_KEY_ALGORITHMIA)
        algo = client.algo('web/WikipediaParser/0.1.2')
        algo.set_options(timeout=300)
        return algo.pipe(m_input).result[0]

    def limpa_conteudo(self):
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
        self.conteudo_limpo = texto_limpo

    def quebra_em_sentences(self):
        """
        Divide o conteudo limpo,
        em uma lista de sentenças lógicas.
        """
        seg = pysbd.Segmenter(language="en", clean=False)
        quebrado = seg.segment(self.conteudo_limpo)
        self.sentences = quebrado[:self.dados["input"]["tamanhoSlide"]]

    def cria_keywords(self):
        """
        A partir de uma frase, são definidas as keywords dela.
        """
        n_senteces = []
        for sentence in self.sentences:
            analise = self.watson.analyze_str(sentence)
            keywords = [keyword["text"] for keyword in analise["keywords"]]
            model_sentence = {"text": sentence,
                              "keywords": keywords,
                              "images": []}
            n_senteces.append(model_sentence)
        self.sentences = n_senteces

    def traduzir_sentences(self):
        """
        Traduz as sentenças para português.
        """
        n_sentences = []
        for sentence in self.sentences:
            sentence["text"] = traduz(sentence["text"], 'pt')
            n_sentences.append(sentence)
        self.sentences = n_sentences

    def save(self):
        """
        Salva o conteudo tratado no documento,
        dadosSentences.json
        """
        geral = {"sentences": self.sentences, "input": self.dados["input"]}
        with open('Documents\\dados.json', 'w',
                  encoding='utf-8') as outfile:
            json.dump(geral, outfile, indent=2,
                      ensure_ascii=False)

    def load(self):
        """
        Importa os dados de input do usuário
        """
        with open('Documents\\dados.json', 'r', encoding='utf-8') as j:
            json_data = json.load(j)
            self.dados = json_data


if __name__ == '__main__':
    texto = Texto()
