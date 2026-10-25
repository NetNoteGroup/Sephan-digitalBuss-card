"""
write_nfc_vcard.py
Writes the Sephann Enterprises vCard directly onto a blank NFC tag, so
tapping the card saves the contact straight away -- fully offline, no
webpage or internet connection needed on either phone.

Trade-off vs write_nfc_url.py: if any detail changes (phone, email,
hours) you'll need to rewrite every physical tag, since the data lives
on the chip itself rather than on a page you control.

Needs an NTAG215 or NTAG216 tag -- a vCard this size (~350-450 bytes)
will NOT fit on the smaller NTAG213 (144 bytes usable).

Hardware + setup: same as write_nfc_url.py (a supported USB NFC reader
such as the ACR122U, plus `pip install nfcpy`).

Usage:
    python write_nfc_vcard.py
"""

import nfc
import ndef

from vcard import build_vcard


def write_vcard_to_tag() -> None:
    vcard_bytes = build_vcard().encode("utf-8")
    print(f"vCard size: {len(vcard_bytes)} bytes "
          f"(NTAG213=144B, NTAG215=504B, NTAG216=888B usable)")

    def on_connect(tag):
        print(f"Tag detected: {tag}")

        if tag.ndef is None:
            print("This tag is not NDEF-formatted, or isn't writable.")
            return True

        if not tag.ndef.writeable:
            print("This tag is read-only -- can't write to it.")
            return True

        if len(vcard_bytes) > tag.ndef.capacity:
            print(f"vCard ({len(vcard_bytes)}B) is bigger than this tag's "
                  f"capacity ({tag.ndef.capacity}B). Use a larger tag "
                  f"(NTAG216) or switch to write_nfc_url.py instead.")
            return True

        # Stored as an NDEF MIME Media record with type "text/vcard",
        # exactly how phones expect a scanned vCard to be packaged.
        record = ndef.Record("text/vcard", "sephann", vcard_bytes)
        tag.ndef.records = [record]
        print("Success: vCard written to tag.")
        return True

    print("Hold a blank NFC tag against the reader...")
    clf = nfc.ContactlessFrontend("usb")
    try:
        clf.connect(rdwr={"on-connect": on_connect})
    finally:
        clf.close()


if __name__ == "__main__":
    write_vcard_to_tag()