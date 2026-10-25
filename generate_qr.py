"""
generate_qr.py
Generates the Sephann Enterprises QR code as a PNG image.

Setup (one time):
    pip install "qrcode[pil]"

Two modes:

1. URL mode (recommended once your card page is hosted online).
   The QR just points to your live page, so editing the page later
   updates every printed QR / NFC card automatically -- nothing to
   reprint.

       python generate_qr.py --url https://yourdomain.com/sephann

2. vCard mode (works today, no hosting needed).
   The QR encodes the full contact card directly, so scanning it
   saves the contact straight away, offline, no webpage required.
   Downside: if a phone number changes, every printed QR is outdated
   and has to be reprinted.

       python generate_qr.py --vcard

Output: sephann_qr.png in the current folder.
"""

import argparse

import qrcode
from qrcode.constants import ERROR_CORRECT_M

from vcard import build_vcard

BRAND_DARK = "#17111c"   # matches the card's ink background
BRAND_LIGHT = "#f5efe9"  # matches the card's cream


def make_qr(data: str, out_path: str = "sephann_qr.png") -> str:
    qr = qrcode.QRCode(
        version=None,                 # auto-size to fit the data
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=BRAND_DARK, back_color=BRAND_LIGHT)
    img.save(out_path)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate the Sephann Enterprises QR code")
    parser.add_argument("--url", help="Live URL to encode (recommended once hosted)")
    parser.add_argument("--vcard", action="store_true", help="Encode the vCard directly instead of a URL")
    parser.add_argument("--out", default="sephann_qr.png", help="Output PNG filename")
    args = parser.parse_args()

    if args.url:
        data = args.url
    elif args.vcard:
        data = build_vcard()
    else:
        parser.error("Pass either --url <link> or --vcard")
        return

    path = make_qr(data, args.out)
    print(f"QR code saved to {path}")


if __name__ == "__main__":
    main()