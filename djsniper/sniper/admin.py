from django.contrib import admin
from .models import NFTProject, NFT, NFTTrait, NFTAttribute


class NFTAdmin(admin.ModelAdmin):
    list_display = ["nft_id", "rank", "rarity_score"]
    search_fields = ["nft_id__exact"]


class NFTAttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]
    list_filter = ["name"]


admin.site.register(NFTProject)
admin.site.register(NFTTrait)
admin.site.register(NFT, NFTAdmin)
admin.site.register(NFTAttribute, NFTAttributeAdmin)
