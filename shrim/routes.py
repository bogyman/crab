from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls

from shrim import views

routes = [
    Route('/reservations/list', 'GET', views.reservations_list),
    Route('/reservations/{reservation_id}', 'GET', views.reservation_view),
    Route('/reservations/', 'POST', views.reservation_create),
    Route('/reservations/{reservation_id}', 'PUT', views.reservation_edit),
    Route('/reservations/{reservation_id}', 'PATCH', views.reservation_update),
    Route('/reservations/{reservation_id}', 'DELETE', views.reservation_delete),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
