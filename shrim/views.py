import typing

from shrim.models import Reservation


async def reservations_list() -> typing.List[Reservation]:
    pass


async def reservation_view(reservation_id) -> Reservation:
    pass


async def reservation_create(reservation: Reservation) -> Reservation:
    pass


async def reservation_edit(reservation_id) -> Reservation:
    pass


async def reservation_update(reservation_id) -> Reservation:
    pass


async def reservation_delete(reservation_id) -> Reservation:
    pass
