from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.data.__contains__('non_field_errors'):
            non_field_errors = response.data.pop('non_field_errors')
            response.data['errors'] = ''.join(non_field_errors)
    return response
