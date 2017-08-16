from apistar import typesystem


class Date(typesystem.Integer):
    pass


class ReservationType(typesystem.Object):
    properties = {
        'id': typesystem.integer(minimum=1),
        'first_name': typesystem.string(max_length=100),
        'last_name': typesystem.string(max_length=100),
        'room': typesystem.integer(minimum=1),
        'start_date': Date,
        'end_date': Date,
    }