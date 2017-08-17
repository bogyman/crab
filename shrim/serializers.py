import arrow
from marshmallow import Schema, fields
from marshmallow.fields import Field


class Timestamp(Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return None

        return arrow.get(value).timestamp

    def _deserialize(self, value, attr, data):
        if value is None:
            return None

        return arrow.get(value).datetime


class ReservationSerializer(Schema):
    id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    room = fields.Int()
    start_date = Timestamp()
    end_date = Timestamp()
