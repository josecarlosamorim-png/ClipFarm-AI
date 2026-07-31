from ai.campaign.manager.manager import CampaignManager


manager = CampaignManager()

print()

print("Campanhas encontradas:")

print(manager.list())

print()

campaign = manager.load(
    manager.list()[0]
)

print(campaign)