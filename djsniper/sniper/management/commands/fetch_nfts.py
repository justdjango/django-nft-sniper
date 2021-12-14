from django.core.management.base import BaseCommand
import requests
from web3.main import Web3
from djsniper.sniper.models import NFTProject, NFT, NFTAttribute, NFTTrait

INFURA_PROJECT_ID = ""
INFURA_ENDPOINT = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fetch_nfts(1)

    def fetch_nfts(self, project_id):
        project = NFTProject.objects.get(id=project_id)

        w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))
        contract_instance = w3.eth.contract(
            address=project.contract_address, abi=project.contract_abi
        )

        # Hardcoding only 10 NFTs otherwise it takes long
        for i in range(0, 10):
            ipfs_uri = contract_instance.functions.tokenURI(i).call()
            data = requests.get(
                f"https://ipfs.io/ipfs/{ipfs_uri.split('ipfs://')[1]}"
            ).json()
            nft = NFT.objects.create(
                nft_id=i, project=project, image_url=data["image"].split("ipfs://")[1]
            )
            attributes = data["attributes"]
            for attribute in attributes:
                nft_attribute, created = NFTAttribute.objects.get_or_create(
                    project=project,
                    name=attribute["trait_type"],
                    value=attribute["value"],
                )
                NFTTrait.objects.create(nft=nft, attribute=nft_attribute)
