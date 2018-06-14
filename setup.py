from setuptools import setup, find_packages

setup(
    name="git-credential-github-app-auth",
    author="Alex Ford",
    author_email='fordas@uw.edu',
    license="MIT license",
    description="A git-credential helper for https access via GitHub Apps.",
    url='https://github.com/uw-ipd/git-credential-github-app-auth',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    version='0.1.0',

    packages=find_packages(),
    entry_points={
        'console_scripts' : [
        'git-credential-github-app-auth='
            'git_credential_github_app_auth.cli:cli',
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'click',
        'PyJWT',
        'requests',
        'cryptography',
        'attrs',
    ],

    test_requires=["pytest"],
)
