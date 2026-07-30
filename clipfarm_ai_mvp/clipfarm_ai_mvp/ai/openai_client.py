from ai.llm_interface import LLMInterface


class OpenAIClient(LLMInterface):

    def analyze_segment(self, segment: dict) -> dict:

        return {
            "score": 85,
            "title": "Título sugerido",
            "category": "Educação",
            "confidence": 0.90,
            "reason": "Resposta simulada"
        }
