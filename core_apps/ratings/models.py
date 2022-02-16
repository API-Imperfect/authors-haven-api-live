from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Rating(TimeStampedUUIDModel):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("poor")
        RATING_2 = 2, _("fair")
        RATING_3 = 3, _("good")
        RATING_4 = 4, _("very good")
        RATING_5 = 5, _("excellent")

    article = models.ForeignKey(
        "articles.Article", related_name="article_ratings", on_delete=models.CASCADE
    )
    rated_by = models.ForeignKey(
        User, related_name="user_who_rated", on_delete=models.CASCADE
    )
    value = models.IntegerField(
        verbose_name=_("rating value"),
        choices=Range.choices,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField(verbose_name=_("rating review"), blank=True)

    class Meta:
        unique_together = ["rated_by", "article"]

    def __str__(self):
        return f"{self.article.title} rated at {self.value}"
