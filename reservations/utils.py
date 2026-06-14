def can_view_all_reservations(user):
    return user.has_perm(
        "reservations.view_all_reservations"
    )