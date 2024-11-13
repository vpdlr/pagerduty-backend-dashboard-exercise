from ..db import db
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    @staticmethod
    def add_all(entities):
        try:
            # Use session.merge to either insert or update each entity
            for entity in entities:
                db.session.merge(entity)  # Automatically handles insert or update based on primary key
            db.session.commit()
        except Exception as e:
            print(f"Error storing entities: {str(e)}")
            db.session.rollback()
            raise