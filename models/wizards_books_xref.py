from db import db


wizards_books_association_table = db.Table(
    "WizardsBooksAssociation",
    db.Model.metadata,
    db.Column("wizard_id", db.ForeignKey("Wizards.wizard_id", ondelete="CASCADE"), primary_key=True),
    db.Column("book_id", db.ForeignKey("Books.book_id", ondelete="CASCADE"), primary_key=True)
)
