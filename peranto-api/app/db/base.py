# import all models so that base has them before being
# imported by Alembic

from app.db.base_class import Base
from app.models.user import User
from app.models.photo import Photo
from app.models.passport import Passport
from app.models.curp import Curp