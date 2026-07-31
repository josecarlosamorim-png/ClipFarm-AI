import json
from dataclasses import asdict
from pathlib import Path


class CampaignWriter:

    def save(self, campaign, output_file):

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                asdict(campaign),
                f,
                indent=4,
                ensure_ascii=False
            )