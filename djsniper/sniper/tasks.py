import requests
from time import sleep
from web3.main import Web3

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from django.db.models import OuterRef, Func, Subquery

from djsniper.sniper.models import NFTProject, NFT, NFTAttribute, NFTTrait

INFURA_PROJECT_ID = ""
INFURA_ENDPOINT = f"https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}"


@shared_task
def rank_nfts_task(project_id):
    project = NFTProject.objects.get(id=project_id)

    # calculate sum of NFT trait types
    trait_count_subquery = (
        NFTTrait.objects.filter(attribute=OuterRef("id"))
        .order_by()
        .annotate(count=Func("id", function="Count"))
        .values("count")
    )

    attributes = NFTAttribute.objects.all().annotate(
        trait_count=Subquery(trait_count_subquery)
    )

    # Group traits under each type
    trait_type_map = {}
    for i in attributes:
        if i.name in trait_type_map.keys():
            trait_type_map[i.name][i.value] = i.trait_count
        else:
            trait_type_map[i.name] = {i.value: i.trait_count}

    # Calculate rarity
    """
    [Rarity Score for a Trait Value] = 1 / ([Number of Items with that Trait Value] / [Total Number of Items in Collection])
    """

    for nft in project.nfts.all():
        # fetch all traits for NFT
        total_score = 0

        for nft_attribute in nft.nft_attributes.all():
            trait_name = nft_attribute.attribute.name
            trait_value = nft_attribute.attribute.value

            # Number of Items with that Trait Value
            trait_sum = trait_type_map[trait_name][trait_value]

            rarity_score = 1 / (trait_sum / project.number_of_nfts)

            nft_attribute.rarity_score = rarity_score
            nft_attribute.save()

            total_score += rarity_score

        nft.rarity_score = total_score
        nft.save()

    # Rank NFTs
    for index, nft in enumerate(project.nfts.all().order_by("-rarity_score")):
        nft.rank = index + 1
        nft.save()


@shared_task(bind=True)
def fetch_nfts_task(self, project_id):
    progress_recorder = ProgressRecorder(self)
    project = NFTProject.objects.get(id=project_id)

    w3 = Web3(Web3.HTTPProvider(INFURA_ENDPOINT))
    contract_instance = w3.eth.contract(
        address=project.contract_address, abi=project.contract_abi
    )

    for i in range(0, project.number_of_nfts):
        print("Fetching NFT ...", i)
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
                project=project, name=attribute["trait_type"], value=attribute["value"]
            )
            NFTTrait.objects.create(nft=nft, attribute=nft_attribute)
        progress_recorder.set_progress(i + 1, project.number_of_nfts)
        sleep(1)

    # Call rank function
    rank_nfts_task(project_id)
