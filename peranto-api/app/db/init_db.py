import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base
from app.core.config import settings

logger = logging.getLogger(__name__)

PHOTOS = [
    {
        "id": 1,
        "label": "Juan Perez",
        "source": "Peranto ID",
        "url": "http://photo1.png",
    },
]


# Make sure all SQL Alchemy models are imported (app.db.base) before initializing,
# otherwise Alembic might fail to initialize realtionships property
# for more details see:https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def init_db(db: Session) -> None:
    # Tables should be created with Alebix migrations
    # But if you dont want to use migrations, create
    # The tables uncommenting the following lines
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email= settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="INITIAL super firstname", 
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)

        else:
            logger.warning(
                "Superuser already exists in the database. Skipping creation."
                f"Email: {settings.FIRST_SUPERUSER} already exists in the database."
            )

        if not user.photo:
            for photo in PHOTOS:
                photo_in = schemas.PhotoCreate(
                    label=photo["label"],
                    source=photo["source"],
                    url=photo["url"],
                    owner_id=user.id,
                )
                crud.photo.create(db=db, obj_in=photo_in)

    else:
        logger.warning(
            "No superuser defined in the environment. Skipping creation."
            
            "Need to be created manually."
            "eg. of env FIRST_SUPERUSER=admin@email.com"
        )