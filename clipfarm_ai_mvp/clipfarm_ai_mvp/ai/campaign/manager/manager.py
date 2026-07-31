from .loader import CampaignLoader
from .repository import CampaignRepository


class CampaignManager:

    def __init__(self):

        self.loader = CampaignLoader()

        self.repository = CampaignRepository()

    def list(self):

        return self.repository.list_campaigns()

    def load(
        self,
        campaign_name: str,
    ):

        folder = self.repository.get_folder(
            campaign_name
        )

        return self.loader.load(folder)