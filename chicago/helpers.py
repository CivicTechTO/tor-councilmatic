def topic_classifier(bill) :
    title = bill.description.lower()

    tags = []

    # Determine whether city or ward matters.
    # If list is empty, it's city-wide
    if not bill.wards:
        tags = tags + ["City Matters"]
    else:
        tags = tags + ["Ward Matters"]

    routine_codes = ['MM', 'BL']
    if any(code in bill.identifier for code in routine_codes):
        return tags + ['Member Motion']

    if 'RM' in bill.identifier:
        return tags + ['Routine']

    if 'CC' in bill.identifier:
        return tags + ['New Business']

    if 'IA' in bill.identifier:
        return tags + ['Administrative Inquiry']

    # If Ward=all tag 'City Matters'

    # If Ward=n+ tag 'Ward Matters'

    return tags + ['Unclassified']
