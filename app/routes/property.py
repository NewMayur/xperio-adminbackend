from flask import current_app
from flask import request, jsonify, url_for

from app.schema.Room import Room
from server import app, bcrypt
from app.schema.User import User
from app.schema.Property import Property, PropertyContact
from app.schema.Building import Building, Floor
from app.extensions.db import db
from app.extensions.responses import response_base
import base64
import uuid
from app.extensions.utils import save_base64_file


@app.route("/property/create", methods=["POST"])
def property():
    property_exist = Property.query.all()
    print(property_exist)
    if len(property_exist) > 0:
        return response_base(message="Property already exists", status=409, data=[])
    else:
        pass
    # Save image to file system
    if request.json["banner_base64"] != "":
        banner_path = save_base64_file(request.json["banner_base64"])
    else:
        pass
    if request.json["logo_base64"] != "":
        logo_path = save_base64_file(request.json["logo_base64"])
    else:
        pass
    property = Property(
        name=request.json["name"],
        property_type_master_id=request.json["property_master_id"],
        country=request.json["country"],
        state=request.json["state"],
        city=request.json["city"],
        address1=request.json["address1"],
        address2=request.json["address2"],
        banner_image_path=banner_path,
        logo_image_path=logo_path,
        zip_code=request.json["zip_code"],
    )
    db.session.add(property)
    db.session.flush()
    contact = PropertyContact(
        name=request.json["primary_contact_name"],
        email=request.json["primary_contact_email"],
        phone_number=request.json["primary_contact_contact_number"],
        job_title=request.json["primary_contact_job_title"],
        phone_number_code=request.json["primary_contact_phone_number_code"],
        property_id=property.id,
    )
    db.session.add(contact)
    db.session.commit()

    return response_base(message="Success", status=200, data=[property.id])


@app.route("/property/view", methods=["POST"])
def property_fetch():
    property = Property.query.filter_by(id=request.json["property_id"]).first()
    if not property:
        return response_base(message="Failed", status=404, data=[])
    data = {
        "name": property.name,
        "property_type": property.property_type.name,
        "property_master_id": property.property_type_master_id,
        "country": property.country,
        # "country_id": property.country_master_id,
        "state": property.state,
        # "state_id": property.state_master_id,
        "city": property.city,
        "zip_code": property.zip_code,
        # "city_id": property.city_master_id,
        "address1": property.address1,
        "address2": property.address2,
        "primary_contact_name": property.property_contact[0].name,
        "primary_contact_job_title": property.property_contact[0].job_title,
        "primary_contact_email": property.property_contact[0].email,
        "primary_contact_contact_number": property.property_contact[0].phone_number,
        "primary_contact_contact_number_code": property.property_contact[
            0
        ].phone_number_code,
        "banner_base64": app.config["IMAGE_URL"] + property.banner_image_path,
        "logo_base64": app.config["IMAGE_URL"] + property.logo_image_path,
        # "banner_url": property.banner_image_path,
    }
    return response_base(message="Success", status=200, data=[data])


@app.route("/property/list", methods=["GET"])
def property_list():
    properties = Property.query.all()
    if len(properties) == 0:
        return response_base(message="Failed", status=404, data=[])
    else:
        pass
    property_list = []
    for property in properties:
        buildings = Building.query.filter_by(property_id=property.id).all()
        # print(buildings.floors)
        no_of_buildings = len(buildings)
        no_of_floors = 0
        no_of_rooms = 0
        for building in buildings:
            for floor in building.floors:
                no_of_floors = no_of_floors + 1
                no_of_rooms = no_of_rooms + len(floor.rooms)
        print(no_of_floors)
        print(no_of_rooms)
        print(no_of_buildings)
        data = {
            "property_id": property.id,
            "name": property.name,
            "property_type": property.property_type.name,
            "property_master_id": property.property_type_master_id,
            "country": property.country,
            # "country_id": property.country_master_id,
            "state": property.state,
            # "state_id": property.state_master_id,
            "city": property.city,
            "zip_code": property.zip_code,
            # "city_id": property.city_master_id,
            "address1": property.address1,
            "address2": property.address2,
            "primary_contact_name": property.property_contact[0].name,
            "primary_contact_job_title": property.property_contact[0].job_title,
            "primary_contact_email": property.property_contact[0].email,
            "primary_contact_contact_number": property.property_contact[0].phone_number,
            "primary_contact_contact_number_code": property.property_contact[
                0
            ].phone_number_code,
            "banner_base64": app.config["IMAGE_URL"] + property.banner_image_path,
            "logo_base64": app.config["IMAGE_URL"] + property.logo_image_path,
            "buildings": no_of_buildings,
            "floors": no_of_floors,
            "rooms": no_of_rooms,
            # "banner_url": property.banner_image_path,
        }
        property_list.append(data)
    return response_base(message="Success", status=200, data=property_list)


@app.route("/property/update", methods=["POST"])
def property_update():
    # Save image to file system

    logo_path = ""
    if request.json["banner_base64"] != "":
        banner_path = save_base64_file(request.json["banner_base64"])
    else:
        banner_path = ""
    if request.json["logo_base64"] != "":
        logo_path = save_base64_file(request.json["logo_base64"])
    else:
        logo_path = ""
    property = Property.query.filter_by(id=request.json["property_id"]).first()
    if not property:
        return response_base(message="Failed", status=404, data=[])
    else:
        pass
    property.name = request.json["name"]
    property.property_type_master_id = request.json["property_master_id"]
    property.country = request.json["country"]
    property.state = request.json["state"]
    property.city = request.json["city"]
    property.property_contact[0].phone_number_code = (
        request.json["primary_contact_contact_number"],
    )
    property.zip_code = request.json["zip_code"]
    property.address1 = request.json["address1"]
    property.address2 = request.json["address2"]
    property.banner_image_path = banner_path
    property.logo_image_path = logo_path
    property.property_contact[0].name = request.json["primary_contact_name"]
    property.property_contact[0].job_title = request.json["primary_contact_job_title"]
    property.property_contact[0].email = request.json["primary_contact_email"]
    property.property_contact[0].phone_number = request.json[
        "primary_contact_contact_number"
    ]
    property.property_contact[0].phone_number_code = request.json[
        "primary_contact_contact_number_code"
    ]
    db.session.add(property)
    db.session.commit()
    return response_base(message="Success", status=200, data=[property.id])


@app.route("/property/delete", methods=["DELETE"])
def property_delete():
    property = Property.query.filter_by(id=request.json["property_id"]).first()
    if not property:
        return response_base(message="Failed", status=404, data=[])
    else:
        pass
    buildings = Building.query.filter_by(property_id=property.id).all()
    for building in buildings:
        for floor in building.floors:
            for room in floor.rooms:
                db.session.delete(room)
                for device in room.devices:
                    db.session.delete(device)
            db.session.delete(floor)
        db.session.delete(building)
    db.session.delete(property.property_contact[0])
    db.session.delete(property)
    db.session.commit()
    return response_base(message="Success", status=200, data=[])


@app.route("/images")
def flask_logo():
    return current_app.send_static_file(request.args.get("image_name"))

@app.route("/properties-floors-rooms", methods=["GET"])
def get_properties_floors_rooms():
    properties = Property.query.all()
    if len(properties) == 0:
        return response_base(message="No properties found", status=404, data=[])

    property_data = []
    for property in properties:
        property_info = {
            "property_id": property.id,
            "name": property.name,
            "property_type": property.property_type.name,
            "country": property.country,
            "state": property.state,
            "city": property.city,
            "zip_code": property.zip_code,
            "address1": property.address1,
            "address2": property.address2,
            "floors": [],
        }

        # Fetch floors for each property
        floors = Floor.query.filter_by(property_id=property.id).all()
        for floor in floors:
            floor_info = {
                "floor_id": floor.id,
                "floor_name": f"Floor {floor.number}",
                "rooms": [],
            }

            # Fetch rooms for each floor
            rooms = Room.query.filter_by(floor_id=floor.id).all()
            for room in rooms:
                room_info = {
                    "room_id": room.id,
                    "room_name": "Room " + room.number,
                    # Add more room details as needed
                }
                floor_info["rooms"].append(room_info)

            property_info["floors"].append(floor_info)

        property_data.append(property_info)

    return response_base(message="Success", status=200, data=property_data)