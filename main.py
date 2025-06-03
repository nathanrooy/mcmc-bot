from os import environ
from src import bsky, nostr
from src.utils import create_post


assert environ.get("BSKY_USER") is not None, "could not get bsky username from env"
assert environ.get("BSKY_PSWD") is not None, "could not get bsky password from from env"
assert environ.get("NOSTR_PRIV") is not None, "could not get nostr private key from env"


msg = create_post()

bsky.post(msg)
nostr.post(msg)
