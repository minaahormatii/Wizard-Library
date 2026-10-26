from sqlalchemy.dialects.postgresql import UUID
import uuid

from db import db
from models.wizards_books_xref import wizards_books_association_table


class Books(db.Model):
    __tablename__ = "Books"

    book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Schools.school_id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(), nullable=False, unique=True)
    author = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String())
    rarity_level = db.Column(db.Integer())
    magical_properties = db.Column(db.String())
    available = db.Column(db.Boolean(), default=True)

    school = db.relationship("Schools", back_populates="books")
    spell = db.relationship("Spells", back_populates="book", cascade="all, delete-orphan", uselist=False)
    wizards = db.relationship(
            "Wizards",
            secondary=wizards_books_association_table,
            back_populates="books"
        )
    
    
    def __init__(self, school_id, title, author, subject, rarity_level, magical_properties, available=True):
        self.school_id = school_id
        self.title = title
        self.author = author
        self.subject = subject
        self.rarity_level = rarity_level
        self.magical_properties = magical_properties
        self.available = available