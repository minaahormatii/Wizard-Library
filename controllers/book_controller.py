from flask import jsonify, request

from db import db
from models.school import Schools
from models.wizard import Wizards
from models.book import Books


def add_book():
    post_data = request.form if request.form else request.json

    fields = ["school_id", "title", "author", "subject", "rarity_level", "magical_properties", "available"]
    required_fields = ["school_id", "title", "author"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_book = Books(
        school_id=values["school_id"],
        title=values["title"],
        author=values["author"],
        subject=values["subject"],
        rarity_level=values["rarity_level"],
        magical_properties=values["magical_properties"],
        available=values["available"]
    )

    db.session.add(new_book)
    db.session.commit()

    book_query = db.session.query(Books).filter(Books.book_id == new_book.book_id).first()

    school_query = db.session.query(Schools).filter(Schools.school_id == values["school_id"]).first()

    school_dict = {
        "school_id": school_query.school_id,
        "school_name": school_query.school_name,
        "location": school_query.location,
        "founded_year": school_query.founded_year,
        "headmaster": school_query.headmaster
    }

    book_dict = {
        "book_id": book_query.book_id,
        "school": school_dict,
        "title": book_query.title,
        "author": book_query.author,
        "subject": book_query.subject,
        "rarity_level": book_query.rarity_level,
        "magical_properties": book_query.magical_properties,
        "available": book_query.available
    }

    return jsonify({"message": "book created", "result": book_dict}), 201

def get_all_books():
    query = db.session.query(Books).all()

    book_list = []

    for book in query:
        school_dict = {
            "school_id": book.school.school_id,
            "school_name": book.school.school_name,
            "location": book.school.location,
            "founded_year": book.school.founded_year,
            "headmaster": book.school.headmaster
        }

        wizard_list = []
        for wizard in book.wizards:
            wizard_dict = {
                "wizard_id": wizard.wizard_id,
                "wizard_name": wizard.wizard_name,
                "house": wizard.house,
                "year_enrolled": wizard.year_enrolled,
                "magical_power_level": wizard.magical_power_level,
                "active": wizard.active
            }
            wizard_list.append(wizard_dict)

        if book.spell:
            spell_dict = {
                "spell_id": book.spell.spell_id,
                "spell_name": book.spell.spell_name,
                "incantation": book.spell.incantation,
                "difficulty_level": book.spell.difficulty_level,
                "spell_type": book.spell.spell_type,
                "description": book.spell.description
            }
        else:
            spell_dict = {}

        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "subject": book.subject,
            "rarity_level": book.rarity_level,
            "magical_properties": book.magical_properties,
            "available": book.available,
            "school": school_dict,
            "wizards": wizard_list,
            "spell": spell_dict
        }

        book_list.append(book_dict)

    return jsonify({"message": "books found", "results": book_list}), 200

def get_books_by_wizard_id(wizard_id):
    query = db.session.query(Books).filter(Books.wizards.any(Wizards.wizard_id == wizard_id)).all()

    if not query:
        return jsonify({"message": "books not found"}), 404

    book_list = []
    for book in query:
        if book.school:
            school_dict = {
                "school_id": str(book.school.school_id),
                "school_name": book.school.school_name,
                "location": book.school.location,
                "founded_year": book.school.founded_year,
                "headmaster": book.school.headmaster
            }
        else:
            school_dict = {}

        wizard_list = []
        for wizard in book.wizards:
            wizard_dict = {
                "wizard_id": wizard.wizard_id,
                "wizard_name": wizard.wizard_name,
                "house": wizard.house,
                "year_enrolled": wizard.year_enrolled,
                "magical_power_level": wizard.magical_power_level,
                "active": wizard.active
            }
            wizard_list.append(wizard_dict)

        if book.spell:
            spell_dict = {
                "spell_id": book.spell.spell_id,
                "spell_name": book.spell.spell_name,
                "incantation": book.spell.incantation,
                "difficulty_level": book.spell.difficulty_level,
                "spell_type": book.spell.spell_type,
                "description": book.spell.description
            }
        else:
            spell_dict = {}

        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "subject": book.subject,
            "rarity_level": book.rarity_level,
            "magical_properties": book.magical_properties,
            "available": book.available,
            "school": school_dict,
            "wizards": wizard_list,
            "spell": spell_dict
        }

        book_list.append(book_dict)

    return jsonify({"message": "books found", "results": book_list}), 200

def update_book_by_id(book_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    if not query:
        return jsonify({"message": "book does not exist"}), 404

    query.school_id = post_data.get("school_id", query.school_id)
    query.title = post_data.get("title", query.title)
    query.author = post_data.get("author", query.author)
    query.subject = post_data.get("subject", query.subject)
    query.rarity_level = post_data.get("rarity_level", query.rarity_level)
    query.magical_properties = post_data.get("magical_properties", query.magical_properties)
    query.available = post_data.get("available", query.available)

    db.session.commit()

    school_dict = {
        "school_id": query.school.school_id,
        "school_name": query.school.school_name,
        "location": query.school.location,
        "founded_year": query.school.founded_year,
        "headmaster": query.school.headmaster
    }

    wizard_list = []
    for wizard in query.wizards:
        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "active": wizard.active
        }
        wizard_list.append(wizard_dict)

    if query.spell:
        spell_dict = {
            "spell_id": query.spell.spell_id,
            "spell_name": query.spell.spell_name,
            "incantation": query.spell.incantation,
            "difficulty_level": query.spell.difficulty_level,
            "spell_type": query.spell.spell_type,
            "description": query.spell.description
        }
    else:
        spell_dict = {}

    book_dict = {
        "book_id": query.book_id,
        "school": school_dict,
        "wizards": wizard_list,
        "spell": spell_dict,
        "title": query.title,
        "author": query.author,
        "subject": query.subject,
        "rarity_level": query.rarity_level,
        "magical_properties": query.magical_properties,
        "available": query.available
    }

    return jsonify({"message": "book updated", "result": book_dict}), 200

def delete_book_by_id(book_id):
    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    if not query:
        return jsonify({"message": "book does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete book"}), 400

    return jsonify({"message": "book deleted"}), 200