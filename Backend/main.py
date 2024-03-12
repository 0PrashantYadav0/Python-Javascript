from flask import request, jsonify
from config import app, db
from models import Contact

@app.route('/contacts', methods=["GET"])
def get_contacts():
  contacts = Contact.query.all()
  json_contacts = list(map(lambda x: x.to_json(), contacts))

  return jsonify({"contacts": json_contacts})


@app.route('/create_contact', methods=["POST"])
def create_contact():
  first_name = request.json.get("firstName")
  last_name = request.json.get("lastName")
  email = request.json.get("email")

  if not first_name or not last_name or not email:
    return (jsonify({"message": "You must include a first name, last name, and email"}), 400)
  
  new_contact = Contact(first_name=first_name, last_name=last_name, email=email)

  try:
    db.session.add(new_contact)
    db.session.commit()
  except Exception as e:
    return (jsonify({"message": f"An error occurred: {e}"}), 500)

  return (jsonify({"message": "Contact created successfully"}), 201)


@app.route('/update_contact/<int:user_id>', methods=["PUT"])
def update_contact(user_id):
  first_name = request.json.get("firstName")
  last_name = request.json.get("lastName")
  email = request.json.get("email")

  contact = Contact.query.get(user_id)

  if not contact:
    return (jsonify({"message": "Contact not found"}), 404)

  if first_name:
    contact.first_name = first_name
  if last_name:
    contact.last_name = last_name
  if email:
    contact.email = email

  try:
    db.session.commit()
  except Exception as e:
    return (jsonify({"message": f"An error occurred: {e}"}), 500)

  return (jsonify({"message": "Contact updated successfully"}), 200)


@app.route('/delete_contact/<int:user_id>', methods=["DELETE"])
def delete_contact(user_id):
  contact = Contact.query.get(user_id)

  if not contact:
    return (jsonify({"message": "Contact not found"}), 404)

  try:
    db.session.delete(contact)
    db.session.commit()
  except Exception as e:
    return (jsonify({"message": f"An error occurred: {e}"}), 500)

  return (jsonify({"message": "Contact deleted successfully"}), 200)



if __name__ == "__main__":
  with app.app_context():
    db.create_all()

  app.run(debug=True)