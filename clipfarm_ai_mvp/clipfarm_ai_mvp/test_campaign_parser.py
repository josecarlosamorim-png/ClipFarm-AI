from ai.campaign.parser.parser import CampaignParser

parser = CampaignParser()

campaign = parser.parse("campaigns/moonpay/brief.pdf")

print(campaign)