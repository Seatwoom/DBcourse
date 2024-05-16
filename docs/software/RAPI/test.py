from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        return connection
    except Error as e:
        print(f"Error while connecting to PostgreSQL: {e}")


@app.route('/accesses', methods=['GET'])
def get_accesses():
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM public.\"Accesses\"")
            accesses = cursor.fetchall()
            return jsonify(accesses)
        except Error as e:
            print(f"Error while fetching data from PostgreSQL: {e}")
        finally:
            if connection is not None:
                connection.close()
    else:
        return "Error: Unable to connect to the database"


@app.route('/accesses', methods=['POST'])
def add_access():
    if request.method == 'POST':
        new_access = request.json
        user_id = new_access['user_id']
        permission_id = new_access['permission_id']
        dataset_id = new_access['dataset_id']

        connection = create_connection()
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO public.\"Accesses\" (user_id, permission_id, dataset_id) VALUES (%s, %s, %s)",
                    (user_id, permission_id, dataset_id))
                connection.commit()
                return "Access added successfully"
            except Error as e:
                connection.rollback()
                print(f"Error while inserting data into PostgreSQL: {e}")
            finally:
                if connection is not None:
                    connection.close()
        else:
            return "Error: Unable to connect to the database"


@app.route('/accesses/<int:access_id>', methods=['DELETE'])
def delete_access(access_id):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM public.\"Accesses\" WHERE user_id = %s", (access_id,))
            connection.commit()
            return jsonify({"message": "Access deleted successfully"})
        except Error as e:
            connection.rollback()
            print(f"Error while deleting data from PostgreSQL: {e}")
            return jsonify({"error": "An error occurred while deleting the access"}), 500
        finally:
            if connection is not None:
                connection.close()
    else:
        return jsonify({"error": "Unable to connect to the database"}), 500


@app.route('/accesses/<int:access_id>', methods=['PUT'])
def update_access(access_id):
    if request.method == 'PUT':
        updated_access = request.json
        user_id = updated_access['user_id']
        permission_id = updated_access['permission_id']
        dataset_id = updated_access['dataset_id']

        connection = create_connection()
        if connection is not None:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE public.\"Accesses\" SET user_id = %s, permission_id = %s, dataset_id = %s WHERE user_id = %s",
                    (user_id, permission_id, dataset_id, access_id))
                connection.commit()
                return jsonify({"message": "Access updated successfully"})
            except Error as e:
                connection.rollback()
                print(f"Error while updating data in PostgreSQL: {e}")
                return jsonify({"error": "An error occurred while updating the access"}), 500
            finally:
                if connection is not None:
                    connection.close()
        else:
            return jsonify({"error": "Unable to connect to the database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
