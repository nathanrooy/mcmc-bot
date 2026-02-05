import ssl
import time
from os import _exit, environ

from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey


def post(msg):
    relay_manager = RelayManager()
    for relay in ["relay.damus.io", "nos.lol", "nostr.wine"]:
        relay_manager.add_relay(f"wss://{relay}")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})
    time.sleep(5)

    try:
        private_key = PrivateKey.from_nsec(environ.get("NOSTR_PRIV"))
        event = Event(private_key.public_key.hex(), msg, tags=[], kind=EventKind.TEXT_NOTE)
        private_key.sign_event(event)
        
        print(f"> nostr :: publishing to relays...")
        relay_manager.publish_event(event)
        time.sleep(3)

    except Exception as e:
        print(f"> nostr :: post likely sent, but encountered an error: {e}")

    finally:
        print("> nostr :: closing connections...")
        relay_manager.close_connections()

        # force exit to avoid zombie threads
        _exit(0)
