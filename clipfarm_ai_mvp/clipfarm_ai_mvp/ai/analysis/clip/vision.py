from .models import ClipAnalysis


class VisionAnalyzer:

    def analyze(
        self,
        analysis: ClipAnalysis,
    ) -> ClipAnalysis:

        # Futuramente:
        #
        # - OCR
        # - Logos
        # - Faces
        # - Objetos
        #
        # Por agora devolvemos o objeto.

        return analysis