import json

from flask import Blueprint, request, Response

# from src.repository.memrepo import MemRepo
from src.repository.postgresrepo import PostgresRepo
from src.responses import ResponseTypes
from src.use_cases.snippet_list import snippet_list_use_case
from src.serializers.snippet import SnippetJsonEncoder
from src.requests.snippet_list import build_snippet_list_request

blueprint = Blueprint("snippet", __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}


postgres_configuration = {
    "POSTGRES_USER": os.environ["POSTGRES_USER"],
    "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "POSTGRES_NOSTNAME": os.environ["POSTGRES_HOSTNAME"],
    "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
    "APPLICATION_DB": os.environ["APPLICATION_DB"],
}

snippets = [
    {
        "code": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e",
        "language": "Python",
        "title": "Replace to join",
        "description": "''.join(data)",
        "created_at": "2021-11-13",
    },
    {
        "code": "832b1bed-d4c1-4365-9397-1ba680f309a7",
        "language": "Bash",
        "title": "Commands Docker",
        "description": "sudo service docker start",
        "created_at": "2021-11-12",
    },
    {
        "code": "4119a868-2a1d-414b-9871-a3669aabd0a0",
        "language": "Python",
        "title": "Code Pythonics",
        "description": "if data in datas: print(data)",
        "created_at": "2021-11-12",
    },
    {
        "code": "b1d70ad2-717c-4e01-b550-ae9af9c5cdac",
        "language": "Python",
        "title": "Code Pythonics",
        "description": "for data in datas: print(data)",
        "created_at": "2021-11-11",
    },
]


@blueprint.route("/snippets", methods=["GET"])
def snippet_list():
    qrystr_params = {
        "filters": {},
    }

    for arg, values in request.args.items():
        if arg.startswith("filter_"):
            qrystr_params["filters"][arg.replace("filter_", "")] = values

    request_object = build_snippet_list_request(filters=qrystr_params["filters"])

    #repo = MemRepo(snippets)
    repo = PostgresRepo(postgres_configuration)
    response = snippet_list_use_case(repo, request_object)

    return Response(
        json.dumps(response.value, cls=SnippetJsonEncoder),
        mimetype="application/json",
        status=STATUS_CODES[response.type],
    )
