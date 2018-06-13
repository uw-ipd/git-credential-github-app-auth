import pytest

from ..helper import credential_helper

def test_credential_helper():
    test_tokens = {"test": "testtoken", "test2": "testtoken2"}

    ssh = """
host=github.com
protocol=ssh
    """.strip()

    assert ssh == credential_helper(ssh, test_tokens.get)

    no_path = """
host=github.com
protocol=https
    """.strip()

    assert no_path == credential_helper(no_path, test_tokens.get)

    test_repo = """
host=github.com
protocol=https
path=test/repo
    """.strip()
    test_repo_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert test_repo_expected == credential_helper(test_repo, test_tokens.get)

    test2_repo = """
host=github.com
protocol=https
path=test2/repo
    """.strip()
    test2_repo_expected = """
host=github.com
protocol=https
path=test2/repo
username=x-access-token
password=testtoken2
    """.strip()

    assert test2_repo_expected == credential_helper(test2_repo, test_tokens.get)

    override_name = """
host=github.com
protocol=https
path=test/repo
username=user
    """.strip()
    override_name_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert override_name_expected == credential_helper(override_name, test_tokens.get)

    invalid_input = """
host=github.com
wat
    """.strip()
    with pytest.raises(ValueError):
        credential_helper(invalid_input, test_tokens.get)
