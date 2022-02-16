from rest_framework import serializers

from core_apps.articles.models import Article, ArticleViews
from core_apps.comments.serializers import CommentListSerializer
from core_apps.ratings.serializers import RatingSerializer

from .custom_tag_field import TagRelatedField


class ArticleViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleViews
        exclude = ["updated_at", "pkid"]


class ArticleSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField(read_only=True)
    banner_image = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField(source="article_read_time")
    ratings = serializers.SerializerMethodField()
    num_ratings = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField(source="get_average_rating")
    likes = serializers.ReadOnlyField(source="article_reactions.likes")
    dislikes = serializers.ReadOnlyField(source="article_reactions.dislikes")
    tagList = TagRelatedField(many=True, required=False, source="tags")
    comments = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_banner_image(self, obj):
        return obj.banner_image.url

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_author_info(self, obj):
        return {
            "username": obj.author.username,
            "fullname": obj.author.get_full_name,
            "about_me": obj.author.profile.about_me,
            "profile_photo": obj.author.profile.profile_photo.url,
            "email": obj.author.email,
            "twitter_handle": obj.author.profile.twitter_handle,
        }

    def get_ratings(self, obj):
        reviews = obj.article_ratings.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data

    def get_num_ratings(self, obj):
        num_reviews = obj.article_ratings.all().count()
        return num_reviews

    def get_comments(self, obj):
        comments = obj.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return serializer.data

    def get_num_comments(self, obj):
        num_comments = obj.comments.all().count()
        return num_comments

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tagList",
            "description",
            "body",
            "banner_image",
            "read_time",
            "author_info",
            "likes",
            "dislikes",
            "ratings",
            "num_ratings",
            "average_rating",
            "views",
            "num_comments",
            "comments",
            "created_at",
            "updated_at",
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    banner_image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ["updated_at", "pkid"]

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_banner_image(self, obj):
        return obj.banner_image.url


class ArticleUpdateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["title", "description", "body", "banner_image", "tags", "updated_at"]

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
