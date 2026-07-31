from .branding import validate_branding
from .content import validate_content
from .keywords import validate_keywords

from .duration import validate_duration
from .language import validate_language

from .scoring import merge_results


class CampaignValidator:

    def validate(
        self,
        campaign,
        clip,
    ):

        results = [

            # Branding
            validate_branding(
                campaign,
                clip,
            ),

            # Conteúdo
            validate_content(
                campaign,
                clip,
            ),

            # Keywords
            validate_keywords(
                campaign,
                clip,
            ),

            # Duração
            validate_duration(
                campaign,
                clip,
            ),

            # Idioma
            validate_language(
                campaign,
                clip,
            ),

        ]

        return merge_results(results)