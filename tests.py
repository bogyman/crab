import arrow
import factory

from apistar.test import TestClient
from faker import Factory
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app
from shrim import models
from shrim._sqlalchemy_base import Base

fake = Factory.create()
engine = create_engine('sqlite:///db.db')
session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)


class ReservationFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = fake.first_name()
    last_name = fake.last_name()
    room = factory.Sequence(lambda n: n+1)
    start_date = arrow.utcnow().shift(days=-1).datetime
    end_date = arrow.utcnow().datetime

    class Meta:
        model = models.Reservation
        sqlalchemy_session = session
        sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_COMMIT


def test_post():
    client = TestClient(app)

    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "room": 1,
        "start_date": arrow.utcnow().shift(days=-1).timestamp,
        "end_date": arrow.utcnow().timestamp,
    }
    response = client.post('/reservations/', json=data)
    assert response.status_code == 200

    resp_data = response.json()

    assert resp_data.pop('id')

    assert resp_data == data


def test_view():
    client = TestClient(app)

    reservation = ReservationFactory.create()

    print(reservation.id)
    response = client.get('/reservations/{}'.format(reservation.id))

    assert response.status_code == 200

    resp_data = response.json()

    assert resp_data['first_name'] == reservation.first_name
    assert resp_data['last_name'] == reservation.last_name
    assert resp_data['room'] == reservation.room
    assert resp_data['start_date'] == arrow.get(reservation.start_date).timestamp
    assert resp_data['end_date'] == arrow.get(reservation.end_date).timestamp


def test_update():
    client = TestClient(app)

    reservation = ReservationFactory.create()

    new_start_date = arrow.utcnow().shift(days=-2)

    response = client.patch(
        url='/reservations/{}'.format(reservation.id),
        json={
            "start_date": new_start_date.timestamp
        }
    )

    assert response.status_code == 200

    resp_data = response.json()

    assert resp_data['start_date'] == new_start_date.timestamp


def test_delete():
    client = TestClient(app)

    reservation = ReservationFactory.create()

    response = client.delete(
        url='/reservations/{}'.format(reservation.id),
    )

    assert response.status_code == 200

    response = client.get(
        url='/reservations/{}'.format(reservation.id),
    )

    assert response.status_code == 404


def test_search():
    client = TestClient(app)

    reservations_in = [
        ReservationFactory.create(
            start_date=arrow.utcnow().shift(days=-i).datetime,
            end_date=arrow.utcnow().shift(days=-i + 2).datetime
        )
        for i in range(4)
    ]

    reservations_out = [
        ReservationFactory.create(
            start_date=arrow.utcnow().shift(days=-i-10).datetime,
            end_date=arrow.utcnow().shift(days=-i - 8).datetime
        )
        for i in range(2)
    ]

    response = client.get(
        url='/reservations/list',
        data={
            "start_date": arrow.utcnow().shift(days=-6),
            "end_date": arrow.utcnow().shift(days=-2)
        }
    )

    assert response.status_code == 200
