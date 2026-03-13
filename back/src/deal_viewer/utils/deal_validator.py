from datetime import UTC, datetime
from deal_viewer.models.deal_model import (
    REQUIRED_FIELDS,
    AUTOMATIC_FIELDS,
    CONTACT_FIELDS,
)


def validate_and_build_deal(data: dict) -> dict:

    if not isinstance(data, dict):
        raise ValueError("Le payload doit être un objet JSON valide.")

    deal = {}

    # Vérification des champs obligatoires
    for field in REQUIRED_FIELDS:
        if field not in data:
            raise ValueError(f"Champ obligatoire manquant : {field}")
        deal[field] = data[field]

    # Vérification des contacts
    contacts = data.get("contacts")
    if not isinstance(contacts, list) or len(contacts) == 0:
        raise ValueError("Le champ 'contacts' doit être une liste non vide.")

    validated_contacts = []
    for contact in contacts:
        if not isinstance(contact, dict):
            raise ValueError("Chaque contact doit être un objet JSON.")

        validated_contact = {}
        for contact_field in CONTACT_FIELDS:
            if contact_field not in contact:
                raise ValueError(f"Champ obligatoire manquant dans un contact : {contact_field}")
            validated_contact[contact_field] = contact[contact_field]

        # Champs en plus du contact
        for k, v in contact.items():
            if k not in CONTACT_FIELDS:
                validated_contact[k] = v

        validated_contacts.append(validated_contact)

    deal["contacts"] = validated_contacts

    # champs optionnels
    for key, value in data.items():
        # Déjà géré
        if key in REQUIRED_FIELDS or key in AUTOMATIC_FIELDS or key == "contacts":
            continue
        deal[key] = value  

    #Champs automatiques
    deal["createdAt"] = datetime.now(UTC)
    return deal
