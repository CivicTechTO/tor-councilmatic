def topic_classifier(bill) :
    title = bill.description.lower()
    classified = False

    tags = []

    # Determine whether city or ward matters.
    # If list is empty, it's city-wide
    if not bill.wards:
        classified = True
        tags = tags + ["City Matters"]
    else:
        classified = True
        tags = tags + ["Ward Matters"]

    routine_codes = ['RM', 'BL']
    if any(code in bill.identifier for code in routine_codes):
        classified = True
        tags = tags + ['Routine']

    if 'MM' in bill.identifier:
        classified = True
        tags = tags + ['Member Motion']

    if 'CC' in bill.identifier:
        classified = True
        tags = tags + ['New Business']

    if 'IA' in bill.identifier:
        classified = True
        tags = tags + ['Administrative Inquiry']

    if not classified:
        tags = tags + ['Unclassified']

    return tags
