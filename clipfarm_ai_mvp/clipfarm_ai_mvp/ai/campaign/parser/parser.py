import fitz
from pathlib import Path

from .writer import CampaignWriter
from .extractor import RuleExtractor


class CampaignParser:

    def __init__(self):

        self.extractor = RuleExtractor()
        self.writer = CampaignWriter()

    def parse(self, pdf_path):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        # Extrair regras do PDF
        campaign = self.extractor.extract(text)

        # Caminho onde será guardado o JSON
        output = (
            Path(pdf_path)
            .parent
            / "campaign.json"
        )

        # Guardar o JSON
        self.writer.save(
            campaign,
            output
        )

        return campaign