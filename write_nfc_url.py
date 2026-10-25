"""
write_nfc_url.py
Writes a URL onto a blank NFC tag (NTAG213 / NTAG215 / NTAG216) using
nfcpy, so tapping the card with a phone opens that page directly.

This is the RECOMMENDED way to program the physical card: point it at
your hosted digital-card page (see generate_qr.py's --url mode). If you
ever change your phone number or add a new product photo, you edit the
page once -- the tag never needs rewriting.

Hardware needed:
    A USB NFC reader/writer that nfcpy supports, e.g. the ACR122U, or a
    PN532 breakout board wired over USB/serial. Most laptops' built-in
    NFC (if any) is NOT supported by nfcpy -- you need a dedicated reader.

Setup (one time):
    pip install nfcpy
    # Linux: you may also need to add a udev rule, or run with sudo,
    # so nfcpy can access the USB device.

Usage:
    python write_nfc_url.py https://yourdomain.com/sephann
"""

import sys

import nfc
import ndef


def write_url_to_tag(url: str) -> None:
    def on_connect(tag):
        print(f"Tag detected: {tag}")

        if tag.ndef is None:
            print("This tag is not NDEF-formatted, or isn't writable.")
            return True

        if not tag.ndef.writeable:
            print("This tag is read-only -- can't write to it.")
            return True

        record = ndef.UriRecord(url)
        tag.ndef.records = [record]
        print(f"Success: tag now points to {url}")
        return True

    print("Hold a blank NFC tag against the reader...")
    clf = nfc.ContactlessFrontend("usb")
    try:
        clf.connect(rdwr={"on-connect": on_connect})
    finally:
        clf.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python write_nfc_url.py <url>")
        sys.exit(1)
    write_url_to_tag(sys.argv[1])