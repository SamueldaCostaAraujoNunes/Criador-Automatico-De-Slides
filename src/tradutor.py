from googletrans import Translator


def traduz(texto: str, language: str) -> str:
    """
    Traduz um texto para uma determinada lingua.
    """
    translator = Translator()
    traduzido = translator.translate(texto, dest=language)
    return traduzido.text
