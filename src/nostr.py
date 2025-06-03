import ssl
import time
from os import environ

from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey


def post(msg):
    relay_manager = RelayManager()
    for relay in ["relay.damus.io", "nos.lol", "nostr.wine"]:
        relay_manager.add_relay(f"wss://{relay}")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(2)

    private_key = PrivateKey.from_nsec(environ.get("NOSTR_PRIV"))
    public_key = private_key.public_key

    event = Event(public_key.hex(), msg, tags=[], kind=EventKind.TEXT_NOTE)

    private_key.sign_event(event)
    relay_manager.publish_event(event)
    time.sleep(1)

    relay_manager.close_connections()
