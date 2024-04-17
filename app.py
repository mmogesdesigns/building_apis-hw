from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
# local import for db_connection
from connect_db import connect_db, Error


app = Flask(__name__)
app.json.sort_keys= False

ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    member_id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    bench_amount = fields.Int(required= True)
    membership_type = fields.String(required=True)

    class Meta:
        fields= ("member_id","name","email","phone","bench_amount","membership_type")
    # instantiating CustomerSchema class

member_schema = MemberSchema()
members_schema = MemberSchema(many= True)





@app.route('/')
def home():
    return "Welcome to our super cool Fitness Tracker, time to get swoll!"

@app.route('/members', methods=['GET'])
def get_members():
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}),500
        cursor = conn.cursor(dictionary=True) #(dictionary = true) only for GET
        # SQL query to fetch all customers
        query = "SELECT * FROM Members"

        # executing query with cursor
        cursor.execute(query)

        # accessing stored query
        members = cursor.fetchall()

        # use Marshmallow to format the json response
        return members_schema.jsonify(members)
    
    except Error as e:
        # error handling for connection/route issues
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        #checking again for connection object
        if conn and conn.is_connected():
            cursor.close()
            conn.close()  

@app.route('/members', methods = ['POST'])
def add_members():
    try:
        # validate the data follows our structure
        # deserialize the data using marshmallow
        # this gives us a python dictionary
        member_data = member_schema.load(request.json)

    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages),400
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error:" "Database connection failed"}), 500
        cursor = conn.cursor()

        # new customer details, to be sent to our db
        # comes from customer_data which we turn into a python dictionary
        # with .load(request.json)
        new_member = (member_data['name'],member_data['email'],member_data['phone'],member_data['bench_amount'],member_data['membership_status'])

        # SQL query to insert customer data into our database
        query = "INSERT INTO Members (name, email,phone, bench_amount, membership_type)VALUES (%s,%s,%s,%s,%s)"

        # execute the query
        cursor.execute(query, new_member)
        conn.commit()

        # succesfull addition of our customer
        return jsonify({"message": "New member succesfully added"}),201
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        #checking again for connection object
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 

@app.route('/dank_sesh/<int:dank_sesh_id>', methods = ['PUT'])
def update_member(dank_sesh_id):
    try:
        # Validate incoming data
        dank_sesh_data = dank_sesh_schema.load(request.get_json()) 

    except ValidationError as e:
        return jsonify(e.messages), 400

    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        query = "UPDATE DANK_SESH SET name = %s, email = %s, phone = %s, bench_amount %s, membership_type %s WHERE members_id = %s"
        cursor.execute(query, (dank_sesh_data['name'],dank_sesh_data['email'],member_data['phone'],dank_sesh_data['bench_amount'],dank_sesh_data['membership_type']))
        conn.commit()
        return jsonify({"message": "Member updated succesfully"}), 200
    
    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
    #checking again for connection object
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 
# *********** Start Here************************
# DELETE requests
@app.route("/orders/<int:dank_sesh_id>", methods = ['DELETE'])
def delete_member(dank_sesh_id):
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        query = "SELECT * FROM MEMBER WHERE member_id = %s"
        # check if customer exists in db
        cursor.execute(query, dank_sesh_id)
        order = cursor.fetchone()
        if not order:
            return jsonify({"error": "does not exist"}), 404
        
         # If customer exists, we shall delete them :( 
        del_query= "DELETE FROM Dank_sesh where dank_sesh_id= %s"
        cursor.execute(del_query, (dank_sesh_id))
        conn.commit()

        return jsonify({"message": "removed succesfully! "})


    except Error as e:
        print(f"error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        #checking again for connection object
        if conn and conn.is_connected():
            cursor.close()
            conn.close() 



if __name__ =='__main__':
    app.run(debug=True)