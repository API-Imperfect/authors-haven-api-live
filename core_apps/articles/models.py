from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel
from core_apps.ratings.models import Rating

from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()


class Tag(TimeStampedUUIDModel):
    tag = models.CharField(max_length=80)
    slug = models.SlugField(db_index=True, unique=True)

    class Meta:
        ordering = ["tag"]

    def __str__(self):
        return self.tag


class Article(TimeStampedUUIDModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="articles"
    )
    title = models.CharField(verbose_name=_("title"), max_length=250)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.CharField(verbose_name=_("description"), max_length=255)
    body = models.TextField(verbose_name=_("article content"))
    banner_image = models.ImageField(
        verbose_name=_("banner image"), default="/house_sample.jpg"
    )
    tags = models.ManyToManyField(Tag, related_name="articles")
    views = models.IntegerField(verbose_name=_("article views"), default=0)

    def __str__(self):
        return f"{self.author.username}'s article"

    @property
    def list_of_tags(self):
        tags = [tag.tag for tag in self.tags.all()]
        return tags

    @property
    def article_read_time(self):
        time_to_read = ArticleReadTimeEngine(self)
        return time_to_read.get_read_time()

    def get_average_rating(self):
        if Rating.objects.all().count() > 0:
            rating = (
                Rating.objects.filter(article=self.pkid).all().aggregate(Avg("value"))
            )
            return round(rating["value__avg"], 1) if rating["value__avg"] else 0
        return 0


class ArticleViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("ip address"), max_length=250)
    article = models.ForeignKey(
        Article, related_name="article_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.article.title} is - {self.article.views} view(s)"
        )

    class Meta:
        verbose_name = "Total views on Article"
        verbose_name_plural = "Total Article Views"
