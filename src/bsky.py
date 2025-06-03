from os import environ
from atproto import Client


def post(msg):
    client = Client("https://bsky.social")
    client.login(environ.get("BSKY_USER"), environ.get("BSKY_PSWD"))
    client.post(msg)