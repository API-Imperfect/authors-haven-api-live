from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    rated_by = serializers.SerializerMethodField(read_only=True)
    article = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "article", "rated_by", "value"]

    def get_rated_by(self, obj):
        return obj.rated_by.username

    def get_article(self, obj):
        return obj.article.title
