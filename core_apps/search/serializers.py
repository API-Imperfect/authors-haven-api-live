from drf_haystack.serializers import HaystackSerializer

from core_apps.search.search_indexes import ArticleIndex


class ArticleSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [ArticleIndex]

        fields = ["author", "title", "body", "autocomplete", "created_at", "updated_at"]
        ignore_fields = ["autocomplete"]
        field_aliases = {"q": "autocomplete"}
