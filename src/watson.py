from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (Features,
                                                          EntitiesOptions,
                                                          KeywordsOptions)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from secrets import API_KEY_WATSON
import json


class Watson:
    """
    Uma implementação pratica da API do
    natural-language-understanding da Watson IBM
    """
    def __init__(self):
        """
        Inicializa o objeto, autenticando e criando a comunicação inicial.
        """
        authenticator = IAMAuthenticator(API_KEY_WATSON)
        self.service = NaturalLanguageUnderstandingV1(
            version='2018-03-16',
            authenticator=authenticator)
        link = 'https://gateway.watsonplatform.net/' \
               'natural-language-understanding/api'
        self.service.set_service_url(link)

    def analyze_str(self, sentence: str) -> dict:
        """
        É passado um texto para o Watson analizar e ele devolve um dicionário,
        contendo as entidades e palavras chaves do texto.
        """
        response = self.service.analyze(
            text=sentence,
            features=Features(entities=EntitiesOptions(),
                              keywords=KeywordsOptions())
        ).get_result()
        return response

    def analyze_url(self, url_p: str) -> dict:
        """
        É passado um texto para o Watson analizar e ele devolve um dicionário,
        contendo as entidades e palavras chaves do texto.
        """
        response = self.service.analyze(
            url=url_p,
            features=Features(entities=EntitiesOptions(),
                              keywords=KeywordsOptions())
        ).get_result()
        return response


if __name__ == '__main__':
    watson = Watson()
    resposta = watson \
        .analyze_str("O ESP8266 é um microcontrolador "
                     "do fabricante chinês Espressif que "
                     "inclui capacidade de comunicação "
                     "por Wi-Fi.")
    print(json.dumps(resposta, indent=2))
