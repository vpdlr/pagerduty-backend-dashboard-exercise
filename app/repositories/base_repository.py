from ..db import db
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    @staticmethod
    def add_all(entities):
        try:
            db.session.add_all(entities)
            db.session.commit()
        except Exception as e:
            print(f"Error storing entities: {str(e)}")
            db.session.rollback()
            raise