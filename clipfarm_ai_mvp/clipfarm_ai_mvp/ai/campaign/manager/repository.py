from pathlib import Path


class CampaignRepository:

    def __init__(self):

        self.root = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "campaigns"
        )

    def list_campaigns(self):

        if not self.root.exists():

            return []

        folders = []

        for folder in self.root.iterdir():

            if folder.is_dir():

                if (folder / "campaign.json").exists():

                    folders.append(folder.name)

        return sorted(folders)

    def get_folder(
        self,
        name: str,
    ):

        return self.root / name