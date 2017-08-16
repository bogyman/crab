from apistar.frameworks.asyncio import ASyncIOApp as App

from shrim._sqlalchemy_base import Base
from shrim.routes import routes


settings = {
    "DATABASE": {
        "URL": "sqlite:///db.db",
        "METADATA": Base.metadata
    }
}

app = App(routes=routes)
