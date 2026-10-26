from flask import jsonify, request

from db import db
from models.book import Books
from models.spell import Spells


def add_spell():
    post_data = request.form if request.form else request.json

    fields = ["book_id", "spell_name", "incantation", "difficulty_level", "spell_type", "description"]
    required_fields = ["book_id", "spell_name", "incantation", "difficulty_level", "spell_type"]
    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400

        values[field] = field_data

    new_spell = Spells(
        book_id=values["book_id"],
        spell_name=values["spell_name"],
        incantation=values["incantation"],
        difficulty_level=values["difficulty_level"],
        spell_type=values["spell_type"],
        description=values["description"],
    )

    db.session.add(new_spell)
    db.session.commit()

    spell_query = db.session.query(Spells).filter(Spells.spell_id == new_spell.spell_id).first()

    book_query = db.session.query(Books).filter(Books.book_id == values["book_id"]).first()

    book_dict = {
        "book_id": book_query.book_id,
        "title": book_query.title,
        "author": book_query.author,
        "subject": book_query.subject,
        "rarity_level": book_query.rarity_level,
        "magical_properties": book_query.magical_properties,
        "available": book_query.available
    }

    spell_dict = {
        "spell_id": spell_query.spell_id,
        "book": book_dict,
        "spell_name": spell_query.spell_name,
        "incantation": spell_query.incantation,
        "difficulty_level": spell_query.difficulty_level,
        "spell_type": spell_query.spell_type,
        "description": spell_query.description
    }

    return jsonify({"message": "spell created", "result": spell_dict}), 201

def get_all_spells():
    query = db.session.query(Spells).all()

    spell_list = []

    for spell in query:
        book_query = db.session.query(Books).filter(Books.book_id == spell.book_id).first()

        book_dict = {
            "book_id": book_query.book_id,
            "title": book_query.title,
            "author": book_query.author,
            "subject": book_query.subject,
            "rarity_level": book_query.rarity_level,
            "magical_properties": book_query.magical_properties,
            "available": book_query.available
        }

        spell_dict = {
            "spell_id": spell.spell_id,
            "book": book_dict,
            "spell_name": spell.spell_name,
            "incantation": spell.incantation,
            "difficulty_level": spell.difficulty_level,
            "spell_type": spell.spell_type,
            "description": spell.description
        }

        spell_list.append(spell_dict)

    return jsonify({"message": "spells found", "results": spell_list}), 200

def get_spell_by_id(spell_id):
    query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not query:
        return jsonify({"message": "spell does not exist"}), 404

    book_query = db.session.query(Books).filter(Books.book_id == query.book_id).first()

    book_dict = {
        "book_id": book_query.book_id,
        "title": book_query.title,
        "author": book_query.author,
        "subject": book_query.subject,
        "rarity_level": book_query.rarity_level,
        "magical_properties": book_query.magical_properties,
        "available": book_query.available
    }

    spell_dict = {
        "spell_id": query.spell_id,
        "book": book_dict,
        "spell_name": query.spell_name,
        "incantation": query.incantation,
        "difficulty_level": query.difficulty_level,
        "spell_type": query.spell_type,
        "description": query.description
    }

    return jsonify({"message": "spell found", "result": spell_dict}), 200

def update_spell_by_id(spell_id):
    post_data = request.form if request.form else request.json

    query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not query:
        return jsonify({"message": "spell does not exist"}), 404

    query.book_id = post_data.get("book_id", query.book_id)
    query.spell_name = post_data.get("spell_name", query.spell_name)
    query.incantation = post_data.get("incantation", query.incantation)
    query.difficulty_level = post_data.get("difficulty_level", query.difficulty_level)
    query.spell_type = post_data.get("spell_type", query.spell_type)
    query.description = post_data.get("description", query.description)

    db.session.commit()

    book_query = db.session.query(Books).filter(Books.book_id == query.book_id).first()

    book_dict = {
        "book_id": book_query.book_id,
        "title": book_query.title,
        "author": book_query.author,
        "subject": book_query.subject,
        "rarity_level": book_query.rarity_level,
        "magical_properties": book_query.magical_properties,
        "available": book_query.available
    }

    spell_dict = {
        "spell_id": query.spell_id,
        "book": book_dict,
        "spell_name": query.spell_name,
        "incantation": query.incantation,
        "difficulty_level": query.difficulty_level,
        "spell_type": query.spell_type,
        "description": query.description
    }

    return jsonify({"message": "spell updated", "result": spell_dict}), 200

def delete_spell_by_id(spell_id):
    query = db.session.query(Spells).filter(Spells.spell_id == spell_id).first()

    if not query:
        return jsonify({"message": "spell does not exist"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete spell"}), 400

    return jsonify({"message": "spell deleted"}), 200