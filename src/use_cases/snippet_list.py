from src.responses import (
    ResponseSuccess,
    ResponseFailure,
    ResponseTypes, 
    build_response_from_invalid_request
)


def snippet_list_use_case(repo, request):
    if not request:
       return build_response_from_invalid_request(request)
    try:
        snippets = repo.list(filters=request.filters)
        return ResponseSuccess(snippets)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)