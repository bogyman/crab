import typing

import arrow
from apistar import Response, http
from apistar.backends.sqlalchemy_backend import Session
from apistar.exceptions import NotFound, ValidationError

from shrim.models import Reservation
from shrim.serializers import ReservationSerializer
from shrim.types import ReservationType


async def reservations_list(session: Session, query_params: http.QueryParams) -> typing.List[ReservationType]:
    query_params = dict(query_params)
    start_date = query_params.get('start_date')
    end_date = query_params.get('end_date')

    query = session.query(Reservation)

    if start_date:
        query = query.filter(
            Reservation.start_date <= start_date
        )

    if end_date:
        query = query.filter(
            Reservation.end_date >= end_date
        )

    return [ReservationType(ReservationSerializer().dump(obj).data) for obj in query.all()]


async def reservation_view(session: Session, reservation_id: int) -> ReservationType:
    obj = session.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not obj:
        raise NotFound

    return ReservationType(ReservationSerializer().dump(obj).data)


async def reservation_create(session: Session, reservation: ReservationType) -> ReservationType:
    already_booked = session.query(Reservation).filter(
        Reservation.room == reservation['room'],
        Reservation.start_date >= arrow.get(reservation['start_date']).datetime,
        Reservation.end_date <= arrow.get(reservation['end_date']).datetime,
    ).count()

    if already_booked:
        raise ValidationError('this room is already booked for the same dates')

    obj = Reservation(**ReservationSerializer().load(reservation).data)

    session.add(obj)
    session.commit()

    return ReservationType(ReservationSerializer().dump(obj).data)


async def reservation_update(session: Session, reservation_id: int, reservation_data: typing.Dict) -> ReservationType:
    obj = session.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not obj:
        raise NotFound

    for k, v in ReservationSerializer().load(reservation_data).data.items():
        setattr(obj, k, v)

    session.commit()

    return ReservationType(ReservationSerializer().dump(obj).data)


async def reservation_delete(session: Session, reservation_id: int) -> Response:
    obj = session.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not obj:
        raise NotFound

    session.delete(obj)

    return Response({'status': 'ok'})
