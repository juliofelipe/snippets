import pytest
from src.repository import postgresrepo

pytestmark = pytest.mark.integration


def test_repository_list_without_parameters(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_snippets = repo.list()

    assert set([r.code for r in repo_snippets]) == set(
        [r["code"] for r in pg_test_data]
    )


def test_repository_list_with_code_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_snippets = repo.list(
        filters={"code__eq": "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e"}
    )

    assert len(repo_snippets) == 1
    assert repo_snippets[0].code == "f0ca28d5-0ba1-44cd-b47a-d19fe390d03e"


def test_repository_list_with_language_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_snippets = repo.list(filters={"language__eq": "Bash"})

    assert len(repo_snippets) == 1
    assert repo_snippets[0].code == "832b1bed-d4c1-4365-9397-1ba680f309a7"


def test_repository_list_with_title_equal_filter(
    app_configuration, pg_session, pg_test_data
):
    repo = postgresrepo.PostgresRepo(app_configuration)

    repo_snippets = repo.list(filters={"title__eq": "Code Pythonics"})

    assert len(repo_snippets) == 2
    assert set([r.code for r in repo_snippets]) == {
        "4119a868-2a1d-414b-9871-a3669aabd0a0",
        "b1d70ad2-717c-4e01-b550-ae9af9c5cdac",
    }
