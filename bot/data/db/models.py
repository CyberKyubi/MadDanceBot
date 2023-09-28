from sqlalchemy import Column, Integer,  Boolean, Text, TIMESTAMP, Index

from .base import Base


class Publications(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True)
    unix_timestamp = Column(TIMESTAMP, nullable=False)
    title = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    idx_is_published = Index('idx_is_published', is_published)
