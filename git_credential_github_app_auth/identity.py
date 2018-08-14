from typing import Optional, Union

import os
import time
import logging

import attr
import jwt

logger = logging.getLogger(__name__)

@attr.s(frozen=True)
class AppIdentity:
    """Manages a github app id/key pair and signed token generation.

    Manages initialization of an id/key pair from input parameters or, if not
    provided, from the corresponding `GITHUB_APP_AUTH_ID` or
    `GITHUB_APP_AUTH_KEY` environment variable.  Both the id and key may be
    provided as the target value *or* a path in the local filesystem containing
    the value.
    """

    APP_ID_ENV_VAR = "GITHUB_APP_AUTH_ID"
    PRIVATE_KEY_ENV_VAR = "GITHUB_APP_AUTH_KEY"

    @staticmethod
    def _resolve_app_id(app_id: Optional[Union[int, str]] = None):
        """Resolve app id from int id or target file, falling back to `GH_APP_AUTH_ID`."""
        if app_id is None:
            logger.debug("Resolving app_id from env.")

            app_id = os.getenv(AppIdentity.APP_ID_ENV_VAR)
            if app_id is None:
                raise ValueError("Unable to resolve app_id from env: %s" % AppIdentity.APP_ID_ENV_VAR)
            logger.info("Resolved %s to app id: %s", AppIdentity.APP_ID_ENV_VAR, app_id)

        try:
            app_id = int(app_id)
        except ValueError:
            logger.info("Resolved app id to filename: %s", app_id)
            app_id = int(open(app_id, "r").read())

        logger.debug("Resolved app_id: %s", app_id)

        return app_id

    @staticmethod
    def _resolve_key(private_key: Optional[str] = None):
        """Resolve app key from value or target file, falling back to `GH_APP_AUTH_KEY`."""
        if private_key is None:
            logger.debug("Resolving private_key from env.")
            private_key = os.getenv(AppIdentity.PRIVATE_KEY_ENV_VAR)
            if private_key is None:
                raise ValueError("Unable to resolve private_key from env: %s" % AppIdentity.PRIVATE_KEY_ENV_VAR)
            logger.info("Resolved %s to private key.", AppIdentity.PRIVATE_KEY_ENV_VAR)

        if "BEGIN RSA PRIVATE KEY" in private_key:
            logger.info("Resolved private key from value.")
        else:
            logger.info("Resolved private key to filename: %s", private_key)
            private_key = open(private_key, "r").read()

        logger.info("Resolved private key.")
        return private_key

    app_id : int = attr.attrib(
        converter=_resolve_app_id.__func__,
        default = attr.Factory(lambda: AppIdentity._resolve_app_id())
    )
    private_key : str = attr.attrib(
        repr=False,
        converter=_resolve_key.__func__,
        default = attr.Factory(lambda: AppIdentity._resolve_key())
    )

    def jwt(self) -> str:
        """Generate JWT token for the app identity.

        See:
            https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-an-installation
        """
        issue_time = time.time() - 1
        payload = dict(
          iat= int(issue_time),
          exp= int(issue_time + (10 * 60)),
          iss= self.app_id
        )

        logging.debug("Issuing app jwt: %s", payload)

        return jwt.encode(payload, self.private_key, algorithm='RS256').decode()
