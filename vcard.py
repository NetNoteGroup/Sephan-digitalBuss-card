"""
vcard.py
Builds the Sephann Enterprises contact card as a vCard 3.0 string
(RFC 6350 / RFC 2426 format) -- the same standard format your phone's
Contacts app reads when you tap "Save Contact".

Edit the CONTACT dict below any time your details change, then re-run
generate_qr.py / write_nfc_vcard.py to regenerate the QR code or tag.
"""

CONTACT = {
    "org": "Sephann Enterprises",
    "title": "Fashion House",
    "phone_main": "+254798232855",   # also used as WhatsApp number
    "phone_alt": "+254796889283",     # Daniel - owner
    "email": "sephann@gmail.com",
    "city": "Ruiru",
    "area": "Kahawa Sukari",
    "country": "Kenya",
    "note": "The best look, anytime, anywhere. Fashion House in Ruiru, "
            "Kahawa Sukari - Nairobi, Kenya.",
}


def build_vcard(contact: dict = CONTACT) -> str:
    """Return a vCard 3.0 formatted string for the given contact dict."""
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:;{contact['org']};;;",
        f"FN:{contact['org']}",
        f"ORG:{contact['org']}",
        f"TITLE:{contact['title']}",
        f"TEL;TYPE=WORK,VOICE:{contact['phone_main']}",
        f"TEL;TYPE=CELL,WHATSAPP:{contact['phone_main']}",
        f"TEL;TYPE=WORK:{contact['phone_alt']}",
        f"EMAIL;TYPE=INTERNET:{contact['email']}",
        f"ADR;TYPE=WORK:;;{contact['area']};{contact['city']};;;{contact['country']}",
        f"NOTE:{contact['note']}",
        "END:VCARD",
    ]
    # vCard lines are joined with CRLF per spec
    return "\r\n".join(lines) + "\r\n"


if __name__ == "__main__":
    print(build_vcard())