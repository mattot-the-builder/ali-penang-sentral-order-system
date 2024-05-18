def to_RM(amount_in_cents):
    return round(amount_in_cents / 100, 2)


def to_cents(amount_in_RM):
    return round(amount_in_RM * 100)
