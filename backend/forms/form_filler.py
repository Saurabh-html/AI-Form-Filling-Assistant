def fill_form(form_template: dict, extracted_data: dict) -> dict:
    """
    Maps extracted fields to form fields
    """

    filled_form = {
        "form_id": form_template.get("id", "government_form"),  # ✅ CRITICAL FIX
        "title": form_template["title"],
        "fields": {}
    }

    for field in form_template["fields"]:
        value = ""

        if field in extracted_data:
            # Handle nested extraction structure
            if isinstance(extracted_data[field], dict):
                value = extracted_data[field].get("value", "")
            else:
                value = extracted_data[field]

        filled_form["fields"][field] = value

    return filled_form
