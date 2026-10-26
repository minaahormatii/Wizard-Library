from flask import jsonify, request

from db import db
from models.book import Books
from models.school import Schools
from models.wizard import Wizards

def add_wizard():
    post_data = request.form if request.form else request.json

    fields = ["school_id", "wizard_name", "house", "year_enrolled", "magical_power_level"]
    required_fields = ["school_id", "wizard_name", "house", "year_enrolled", "magical_power_level"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_wizard = Wizards(
        school_id=values["school_id"],
        wizard_name=values["wizard_name"],
        house=values["house"],
        year_enrolled=values["year_enrolled"],
        magical_power_level=values["magical_power_level"]
    )

    db.session.add(new_wizard)
    db.session.commit()

    wizard_query = db.session.query(Wizards).filter(Wizards.wizard_name == values["wizard_name"]).first()

    school_query = db.session.query(Schools).filter(Schools.school_id == values["school_id"]).first()

    school_dict = {
        "school_id": school_query.school_id,
        "school_name": school_query.school_name
    }

    wizard_dict = {
        "wizard_id": wizard_query.wizard_id,
        "school": school_dict,
        "wizard_name": wizard_query.wizard_name,
        "house": wizard_query.house,
        "year_enrolled": wizard_query.year_enrolled,
        "magical_power_level": wizard_query.magical_power_level,
        "active": wizard_query.active
    }

    return jsonify({"message": "wizard created", "result": wizard_dict}), 201

def create_wizard_book():
    post_data = request.form if request.form else request.json

    fields = ["wizard_id", "book_id"]
    required_fields = ["wizard_id", "book_id"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    wizard_query = db.session.query(Wizards).filter(Wizards.wizard_id == values["wizard_id"]).first()
    book_query = db.session.query(Books).filter(Books.book_id == values["book_id"]).first()

    if not wizard_query:
        return jsonify({"message": "Wizard does not exist"}), 404

    if not book_query:
        return jsonify({"message": "Book does not exist"}), 404

    if book_query in wizard_query.books:
        return jsonify({"message": "wizard already has this book"}), 400

    wizard_query.books.append(book_query)

    db.session.commit()

    book_list = []
    for book in wizard_query.books:
        book_dict = {
            "book_id": book.book_id,
            "wizard_id": wizard_query.wizard_id,
            "school_id": wizard_query.school.school_id,
            "title": book.title,
            "author": book.author,
            "subject": book.subject,
            "rarity_level": book.rarity_level,
            "magical_properties": book.magical_properties,
            "available": book.available
        }
        book_list.append(book_dict) 

    school_dict = {
        "school_id": wizard_query.school.school_id,
        "school_name": wizard_query.school.school_name,
        "location": wizard_query.school.location,
        "founded_year": wizard_query.school.founded_year,
        "headmaster": wizard_query.school.headmaster
    }

    wizard_dict = {
        "wizard_id": wizard_query.wizard_id,
        "wizard_name": wizard_query.wizard_name,
        "house": wizard_query.house,
        "year_enrolled": wizard_query.year_enrolled,
        "magical_power_level": wizard_query.magical_power_level,
        "school": school_dict,
        "books": book_list,
    }

    return jsonify({"message": "book added to wizard", "result": wizard_dict}), 200

def get_all_wizards():
    query = db.session.query(Wizards).all()

    wizard_list = []

    for wizard in query:
        school_dict = {
            "school_id": wizard.school.school_id,
            "school_name": wizard.school.school_name,
            "location": wizard.school.location,
            "founded_year": wizard.school.founded_year,
            "headmaster": wizard.school.headmaster
        }

        book_list = []
        for book in wizard.books:
            book_dict = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available
            }
            book_list.append(book_dict)

        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "school": school_dict,
            "books": book_list,
        }

        wizard_list.append(wizard_dict)

    return jsonify({"message": "wizards found", "results": wizard_list}), 200

def get_wizard_by_id(wizard_id):
    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard does not exist"}), 404

    school_dict = {
        "school_id": query.school.school_id,
        "school_name": query.school.school_name,
        "location": query.school.location,
        "founded_year": query.school.founded_year,
        "headmaster": query.school.headmaster
    }

    book_list = []
    for book in query.books:
        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "subject": book.subject,
            "rarity_level": book.rarity_level,
            "magical_properties": book.magical_properties,
            "available": book.available
        }
        book_list.append(book_dict)

    wizard_dict = {
        "wizard_id": query.wizard_id,
        "wizard_name": query.wizard_name,
        "house": query.house,
        "year_enrolled": query.year_enrolled,
        "magical_power_level": query.magical_power_level,
        "school": school_dict,
        "books": book_list,
    }

    return jsonify({"message": "wizard found", "result": wizard_dict}), 200

def get_wizards_by_school_id(school_id):
    query = db.session.query(Wizards).filter(Wizards.school_id == school_id).all()

    if not query:
        return jsonify({"message": "no wizards found for this school"}), 404

    wizard_list = []

    for wizard in query:
        school_dict = {
            "school_id": wizard.school.school_id,
            "school_name": wizard.school.school_name,
            "location": wizard.school.location,
            "founded_year": wizard.school.founded_year,
            "headmaster": wizard.school.headmaster
        }

        book_list = []
        for book in wizard.books:
            book_dict = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available
            }
            book_list.append(book_dict)

        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "school": school_dict,
            "books": book_list,
        }

        wizard_list.append(wizard_dict)

    return jsonify({"message": "wizards found", "results": wizard_list}), 200

def get_active_wizards():
    query = db.session.query(Wizards).filter(Wizards.active == True).all()

    wizard_list = []

    for wizard in query:
        school_dict = {
            "school_id": wizard.school.school_id,
            "school_name": wizard.school.school_name,
            "location": wizard.school.location,
            "founded_year": wizard.school.founded_year,
            "headmaster": wizard.school.headmaster
        }

        book_list = []
        for book in wizard.books:
            book_dict = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available
            }
            book_list.append(book_dict)

        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "school": school_dict,
            "books": book_list,
        }

        wizard_list.append(wizard_dict)

    return jsonify({"message": "active wizards found", "results": wizard_list}), 200

def get_wizards_by_house(house):
    query = db.session.query(Wizards).filter(Wizards.house == house).all()

    wizard_list = []

    for wizard in query:
        school_dict = {
            "school_id": wizard.school.school_id,
            "school_name": wizard.school.school_name,
            "location": wizard.school.location,
            "founded_year": wizard.school.founded_year,
            "headmaster": wizard.school.headmaster
        }

        book_list = []
        for book in wizard.books:
            book_dict = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available
            }
            book_list.append(book_dict)

        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "school": school_dict,
            "books": book_list,
        }

        wizard_list.append(wizard_dict)

    return jsonify({"message": f"wizards in {house} house found", "results": wizard_list}), 200

def get_wizards_by_magical_power_level(magical_power_level):
    magical_power_level = int(magical_power_level)
    query = db.session.query(Wizards).filter(Wizards.magical_power_level == magical_power_level).all()

    wizard_list = []

    for wizard in query:
        school_dict = {
            "school_id": wizard.school.school_id,
            "school_name": wizard.school.school_name,
            "location": wizard.school.location,
            "founded_year": wizard.school.founded_year,
            "headmaster": wizard.school.headmaster
        }

        book_list = []
        for book in wizard.books:
            book_dict = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available
            }
            book_list.append(book_dict)

        wizard_dict = {
            "wizard_id": wizard.wizard_id,
            "wizard_name": wizard.wizard_name,
            "house": wizard.house,
            "year_enrolled": wizard.year_enrolled,
            "magical_power_level": wizard.magical_power_level,
            "school": school_dict,
            "books": book_list,
        }

        wizard_list.append(wizard_dict)

    return jsonify({"message": f"wizards with magical power level {magical_power_level} found", "results": wizard_list}), 200

def update_wizard_by_id(wizard_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard does not exist"}), 404

    query.school_id = post_data.get("school_id", query.school_id)
    query.wizard_name = post_data.get("wizard_name", query.wizard_name)
    query.house = post_data.get("house", query.house)
    query.year_enrolled = post_data.get("year_enrolled", query.year_enrolled)
    query.magical_power_level = post_data.get("magical_power_level", query.magical_power_level)
    query.active = post_data.get("active", query.active)

    db.session.commit()

    school_dict = {
        "school_id": query.school.school_id,
        "school_name": query.school.school_name,
        "location": query.school.location,
        "founded_year": query.school.founded_year,
        "headmaster": query.school.headmaster
    }

    book_list = []
    for book in query.books:
        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "subject": book.subject,
            "rarity_level": book.rarity_level,
            "magical_properties": book.magical_properties,
            "available": book.available
        }
        book_list.append(book_dict)

    wizard_dict = {
        "wizard_id": query.wizard_id,
        "wizard_name": query.wizard_name,
        "house": query.house,
        "year_enrolled": query.year_enrolled,
        "magical_power_level": query.magical_power_level,
        "school": school_dict,
        "books": book_list,
    }

    return jsonify({"message": "wizard updated", "result": wizard_dict}), 200

def delete_wizard_by_id(wizard_id):
    query = db.session.query(Wizards).filter(Wizards.wizard_id == wizard_id).first()

    if not query:
        return jsonify({"message": "wizard does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete wizard"}), 400

    return jsonify({"message": "wizard deleted"}), 200