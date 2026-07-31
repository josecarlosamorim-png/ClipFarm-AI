from .models import ClipAnalysis


class AudioAnalyzer:

    def analyze(
        self,
        analysis: ClipAnalysis,
    ) -> ClipAnalysis:

        # Futuramente:
        #
        # - Música
        # - Volume
        # - Silêncio
        #
        # Nesta fase apenas devolvemos
        # o objeto.

        return analysis