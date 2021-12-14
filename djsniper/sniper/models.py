from django.db import models


class NFTProject(models.Model):
    contract_address = models.CharField(max_length=100)
    contract_abi = models.TextField()
    name = models.CharField(max_length=50)  # e.g BAYC
    number_of_nfts = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class NFT(models.Model):
    project = models.ForeignKey(
        NFTProject, on_delete=models.CASCADE, related_name="nfts"
    )
    rarity_score = models.FloatField(null=True)
    nft_id = models.PositiveIntegerField()
    image_url = models.CharField(max_length=200)
    rank = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.project.name}: {self.nft_id}"


class NFTAttribute(models.Model):
    project = models.ForeignKey(
        NFTProject, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"


class NFTTrait(models.Model):
    nft = models.ForeignKey(
        NFT, on_delete=models.CASCADE, related_name="nft_attributes"
    )
    attribute = models.ForeignKey(
        NFTAttribute, on_delete=models.CASCADE, related_name="traits"
    )
    rarity_score = models.FloatField(null=True)

    def __str__(self) -> str:
        return f"{self.attribute.name}: {self.attribute.value}"
