import json
from pathlib import Path

from ai.campaign.models import Campaign


class CampaignLoader:

    def load(self, campaign_folder: Path) -> Campaign:

        json_file = campaign_folder / "campaign.json"

        if not json_file.exists():

            raise FileNotFoundError(json_file)

        with open(
            json_file,
            "r",
            encoding="utf8",
        ) as f:

            data = json.load(f)

        return Campaign(**data)