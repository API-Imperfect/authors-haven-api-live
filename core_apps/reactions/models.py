from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class ReactionManager(models.Manager):
    def likes(self):
        return self.get_queryset().filter(reaction__gt=0).count()

    def dislikes(self):
        return self.get_queryset().filter(reaction__lt=0).count()

    def has_reacted(self):
        request = self.context.get("request")
        if request:
            self.get_queryset().filter(user=request)


class Reaction(TimeStampedUUIDModel):
    class Reactions(models.IntegerChoices):
        LIKE = 1, _("like")
        DISLIKE = -1, _("dislike")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_reactions"
    )
    reaction = models.IntegerField(
        verbose_name=_("like-dislike"), choices=Reactions.choices
    )

    objects = ReactionManager()

    class Meta:
        unique_together = ["user", "article", "reaction"]

    def __str__(self):
        return (
            f"{self.user.username} voted on {self.article.title} with a {self.reaction}"
        )
