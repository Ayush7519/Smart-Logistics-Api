from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)


# -----------------------------------------------------------------------------------------------
# this is the helper for the blacking listing the tokens.
# -----------------------------------------------------------------------------------------------
def blacklist_all_refresh_tokens(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)
