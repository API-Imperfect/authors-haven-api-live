from rest_framework.exceptions import APIException


class CantRateYourArticle(APIException):
    status_code = 403
    default_detail = "You can't rate/review your own article"


class AlreadyRated(APIException):
    status_code = 400
    default_detail = "You have already rated this article"
