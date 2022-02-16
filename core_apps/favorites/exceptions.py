from rest_framework.exceptions import APIException


class AlreadyFavorited(APIException):
    status_code = 400
    default_detail = "You have already favorited this article"
