from datetime import datetime
import json
from . import app_views
from models.user import User
from models.ops import Review
from models.barber import Barber, BarberRating, Style
from flask import request, make_response, jsonify, abort
from api.v1 import db
import uuid


@app_views.route("/barber/rate", methods=["POST"])
def rate_a_barber():
    pass


@app_views.route("/user/hairstyle/", methods=["POST"])
def create_styles():
    """Creates a new hairstyle.

    Return: Information on new style.
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    # data['id'] = str(uuid.uuid4())
    data['id'] = 654

    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if Style.query.filter(Style.name.ilike(data['name'])).first():
        return make_response(jsonify({"error": "Hairstyle exists"}), 400)
    if "image" not in data:
        return make_response(jsonify({"error": "Missing image URI"}), 400)

    style = Style(**data)
    db.session.add(style)
    db.session.commit()

    style_info = {
        "id": style.id,
        "name": style.name,
        "image": style.image,
        "description": style.description,
    }
    return make_response(jsonify(style_info), 201)

@app_views.route("/user/hairstyles/", methods=["GET"])
def get_hairstyles():
    """Gets all hairstyles."""
    hairstyles = []
    for hairstyle in Style.query.all():
        hairstyles.append(hairstyle.to_dict())

    return jsonify(hairstyles)


@app_views.route("/user/hairstyle/<string:hairstyle_nm>", methods=["PUT"])
def update_hairstyle(hairstyle_nm):
    """Updates a hairstyle."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}))

    hairstyle = Style.query.filter(Style.name.ilike(hairstyle_nm)).first()
    if hairstyle is None:
        abort(404)

    for k, v in data.items():
        if k == 'id' or k == 'name':
            continue
        setattr(hairstyle, k, v)

    setattr(hairstyle, "updated_date", datetime.utcnow())

    db.session.add(hairstyle)
    db.session.commit()
    return jsonify(hairstyle.to_dict())


@app_views.route("/user/hairstyle/<style_nm>", methods=["DELETE"])
def remove_styles(style_nm):
    """Removes a hairstyle."""
    style = Style.query.filter(Style.name.ilike(style_nm)).first()
    if style is None:
        abort(404)

    db.session.delete(style)
    db.session.commit()
    del style
    return jsonify({})


# Endpoints for reviews:

@app_views.route("/user/review/", methods=["POST"])
def make_review():
    """Make a review."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}))

    for attr in ["user_id", "barber_id", "review"]:
        if attr not in data:
            return make_response(jsonify({"error": "Missing " + attr}), 400)

    # Ensure that user and barber ids exists
    if User.query.filter_by(id=data["user_id"]).first() is None:
        return make_response(json({"error": "User does not exist"}), 404)
    if Barber.query.filter_by(id=data["user_id"]).first() is None:
        return make_response(json({"error": "Barber does not exist"}), 404)

    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/user/reviews/<string:barber_username>", methods=["GET"])
def get_barberr_reviews(barber_username):
    """Gets all reviews for a barber."""
    barber = Barber.query.filter_by(username=barber_username).first()
    if barber is None:
        return make_response(json({"error": "Barber does not exist"}), 404)

    reviews = []
    for cust in Review.query.filter_by(barber_id=barber.id).all():
        reviews.append(cust.to_dict())

    return jsonify(reviews)


@app_views.route("/user/review/<string:review_id>", methods=["PUT"])
def update_review(review_id):
    """Updates a review."""
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        data = request.get_json()
    else:
        return make_response(jsonify({"error": "Not a JSON"}))

    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        abort(404)

    setattr(review, "review", data["review"])
    setattr(review, "updated_date", datetime.utcnow())

    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict())


@app_views.route("/user/review/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a review"""
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        abort(404)

    db.session.delete(review)
    db.session.commit()
    del review

    return jsonify({})
