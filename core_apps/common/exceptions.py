from rest_framework.views import exception_handler


def common_exception_handler(exc, context):

    response = exception_handler(exc, context)

    handlers = {
        "NotFound": _handle_not_found_error,
        "ValidationError": _handle_generic_error,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_generic_error(exc, context, response):
    status_code = response.status_code
    response.data = {"status_code": status_code, "errors": response.data}

    return response


def _handle_not_found_error(exc, context, response):
    view = context.get("view", None)

    if view and hasattr(view, "queryset") and view.queryset is not None:
        status_code = response.status_code
        error_key = view.queryset.model._meta.verbose_name
        response.data = {
            "status_code": status_code,
            "errors": {error_key: response.data["detail"]},
        }

    else:
        response = _handle_generic_error(exc, context, response)
    return response
