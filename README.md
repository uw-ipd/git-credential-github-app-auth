# `git-credential-github-app-auth`

A minimal [`git-credential`](https://git-scm.com/docs/git-credential)
helper for [https repository access via GitHub
apps](https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/),
providing an alternative to [deploy keys, machine users, and oauth access
tokens](https://developer.github.com/v3/guides/managing-deploy-keys/) in
automated environments.

## Setup

1. Create a [GitHub App](
https://developer.github.com/apps/building-github-apps/creating-a-github-app/)
and [install the application](
https://developer.github.com/apps/managing-github-apps/making-a-github-app-public-or-private/#private-installation-flow)
for your account or organization. Ensure that the app has, at least,
[read-only access to "Repository contents"](
https://developer.github.com/apps/managing-github-apps/editing-a-github-app-s-permissions/)
and [generate a private key](
https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#generating-a-private-key)
for the application.

2. Install `git-credential-github-app-auth` in the integration
   environment.

  ```
  pip install https://github.com/uw-ipd/git-credential-github-app-auth
  ```

3. Add `github-app-auth` as a git-credential helper and ensure that
   `credential.UseHttpPath` is set. The app id and private key may be
   provided as helper arguments or via the `GITHUB_APP_AUTH_ID` and
   `GITHUB_APP_AUTH_KEY` environment variables.

  ```
  git config --global credential.helper github-app-auth --app_id <your_app_id> --private_key <path/to/private-key.pem>
  git config --global credential.UseHttpPath true
  ```

  or

  ```
  git config --global credential.helper github-app-auth 
  git config --global credential.UseHttpPath true

  export GITHUB_APP_AUTH_ID=<your_app_id>
  export GITHUB_APP_AUTH_KEY=<path/to/private-key.pem>
  ```

## Use

The credential helper will provide `https` access credentials for
repositories with valid app installations. The helper configuration can be
verified via `git-credential-github-app-auth -vv [current|token]` and/or:

```
GITHUB_APP_AUTH_DEBUG=2 git credential fill<<URL
url=https://github.com/<org>/<repo>

URL
```
