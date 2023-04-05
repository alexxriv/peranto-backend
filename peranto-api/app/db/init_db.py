import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base
from app.core.config import settings

logger = logging.getLogger(__name__)

PHOTOS = [

    {
        "title": "A photo",
        "description": "A photo description",
        "url": "https://picsum.photos/200/300",
        "owner_id": 1
    },
    {
        "title": "Another photo",
        "description": "Another photo description",
        "url": "https://picsum.photos/200/300",
        "owner_id": 1
    },
    {
        "title": "Yet another photo",
        "description": "Yet another photo description",
        "url": "https://picsum.photos/200/300",
        "owner_id": 1
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
                first_name="INITIAL super user", 
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

        if not user.photos:
            for photo in PHOTOS:
                photo_in = schemas.PhotoCreate(
                    title=photo["title"],
                    description=photo["description"],
                    url=photo["url"],
                    owner_id=photo["owner_id"]
                )
                crud.photo.create(db=db, obj_in=photo_in, owner_id=user.id)

    else:
        logger.warning(
            "No superuser defined in the environment. Skipping creation."
            
            "Need to be created manually."
            "eg. of env FIRST_SUPERUSER=admin@email.com"
        )