from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.comments"
    verbose_name = _("Comments")
