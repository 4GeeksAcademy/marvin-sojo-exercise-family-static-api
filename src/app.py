"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)



# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET all members
@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# POST add new member
@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json() 
    new_member =  {
        "id": body.get("id", jackson_family._generateId()),
        "first_name": body.get("first_name", None),
        "last_name": body.get("last_name", None),
        "age": body.get("age", None),
        "lucky_numbers": body.get("lucky_numbers", None)
    }
    if new_member["last_name"] != None:
        return jsonify({"error": "The last name is generated automatically. Do not send in the body."}), 400
    
    for member in jackson_family._members:
        if new_member["id"] == member["id"]:
            return jsonify({"error": "The id is already in use"}), 400
                                                                         
    accepted_member = jackson_family.add_member(new_member)
    return jsonify(accepted_member), 200
    
# GET one member
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member), 200
    
# DELETE one member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
        member = jackson_family.delete_member(member_id)
        if member is True:
            return jsonify({"done": True}), 200
        return jsonify({"error": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
