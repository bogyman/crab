from apistar import typesystem


class ReservationType(typesystem.Object):
    properties = {
        "id": typesystem.integer(minimum=1, default=None),
        "first_name": typesystem.string(max_length=100),
        "last_name": typesystem.string(max_length=100),
        "room": typesystem.integer(minimum=1),
        "start_date": typesystem.integer(minimum=1),
        "end_date": typesystem.integer(minimum=1),
    }
