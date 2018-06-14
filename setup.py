from setuptools import setup

setup(
    name="git-credential-github-app-auth",
    version='0.1',
    py_modules=['git_credential_github_app_auth'],
    python_requires='>=3.5',
    install_requires=[
        'click',
        'PyJWT',
        'requests',
        'cryptography',
        'attrs',
    ],
    test_requires=["pytest"],
    entry_points='''
        [console_scripts]
        git-credential-github-app-auth=git_credential_github_app_auth.cli:cli
    ''',
)
