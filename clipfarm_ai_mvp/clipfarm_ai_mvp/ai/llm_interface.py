from abc import ABC, abstractmethod


class LLMInterface(ABC):

    @abstractmethod
    def analyze_segment(self, segment: dict) -> dict:
        """
        Analisa um segmento e devolve um dicionário com:
        score, title, category, confidence, reason
        """
        pass
