from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db

class Spells(db.Model):
    __tablename__ = "Spells"

    spell_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Books.book_id", ondelete="CASCADE"), nullable=False)
    spell_name = db.Column(db.String(), nullable=False, unique=True)
    incantation = db.Column(db.String(), nullable=False)
    difficulty_level = db.Column(db.Float(), nullable=False)
    spell_type = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    book = db.relationship("Books", back_populates="spell")


    def __init__(self, book_id, spell_name, incantation, difficulty_level, spell_type, description):
        self.book_id = book_id
        self.spell_name = spell_name
        self.incantation = incantation
        self.difficulty_level = difficulty_level
        self.spell_type = spell_type
        self.description = description
