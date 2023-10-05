from sqlalchemy import Column, Integer,  Boolean, Text, TIMESTAMP, Index

from .base import Base


class Publications(Base):
    __tablename__ = "publications"

    publication_id = Column(Integer, primary_key=True)
    publication_title = Column(Text, nullable=False)
    publication_text = Column(Text, nullable=False)
    publication_at = Column(TIMESTAMP, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    idx_is_published = Index('idx_is_published', is_published)
