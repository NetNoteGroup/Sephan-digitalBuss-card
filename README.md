# Sephann Enterprises — NFC & QR toolkit

Four small Python files. Run them on your own laptop (not in this chat) since
QR generation needs internet access to install a library, and NFC writing
needs a physical USB reader plugged into your machine.

```
vcard.py             shared contact details -- edit this first
generate_qr.py        makes the QR code PNG
write_nfc_url.py      writes a URL to a blank NFC tag  (recommended)
write_nfc_vcard.py    writes the full vCard to a blank NFC tag (offline)
```

## 1. Install

```
pip install -r requirements.txt
```

`nfcpy` is only needed if you're writing physical NFC tags. If you only want
the QR code, `pip install "qrcode[pil]"` is enough.

## 2. Edit your details once

Open `vcard.py` and update the `CONTACT` dictionary if anything changes
(phone, email, location). Both the QR script and the NFC-vCard script pull
from this one file, so you only edit it in one place.

## 3. Generate the QR code

Once your digital card page is hosted somewhere (Netlify, Carrd, your own
domain, etc.), point the QR at it:

```
python generate_qr.py --url https://yourdomain.com/sephann
```

Don't have hosting yet? Generate a QR that works right now, offline:

```
python generate_qr.py --vcard
```

Either way you get `sephann_qr.png`, styled in your brand colors, ready to
print on the physical card, flyers, or the shop window.

## 4. Write the physical NFC card

You need a USB NFC reader/writer nfcpy supports -- the **ACR122U** is the
most common and cheapest (~$15-25 online). Plug it in, then:

```
# Recommended: tag points to your live page, editable forever
python write_nfc_url.py https://yourdomain.com/sephann

# Or: tag holds the contact card directly, works fully offline
# (needs an NTAG215 or NTAG216 blank tag -- NTAG213 is too small)
python write_nfc_vcard.py
```

Hold a blank tag against the reader when the script says to. It'll confirm
once written.

## Which should I actually use -- URL or vCard on the tag?

| | URL on tag | vCard on tag |
|---|---|---|
| Needs hosting | Yes | No |
| Editable later without reprinting/rewriting | Yes | No |
| Works with zero internet on the scanning phone | No | Yes |
| Can show your full page (photos, socials, hours) | Yes | No -- contact only |

For a fashion brand that wants to show off product photos and socials, the
**URL** approach is the better long-term choice -- write it once you have a
hosting link, and use the vCard-only route as a stopgap until then.