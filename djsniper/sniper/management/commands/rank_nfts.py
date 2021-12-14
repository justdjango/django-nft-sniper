from django.core.management.base import BaseCommand
from django.db.models import OuterRef, Func, Subquery
from djsniper.sniper.models import NFTProject, NFTAttribute, NFTTrait


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.rank_nfts(1)

    def rank_nfts(self, project_id):
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
