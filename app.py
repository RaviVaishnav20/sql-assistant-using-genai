import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from backend.upload_to_postgres import upload_to_postgresql
import zipfile
from flask_cors import CORS
from backend.sql_assistant import sql_assistant
import pandas as pd
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'backend', 'datasets', 'uploads')
ALLOWED_EXTENSIONS = {'db', 'sqlite', 'csv', 'xls', 'xlsx', 'json', 'zip', 'asc'}
DB_CRED_FILE = os.path.join(os.getcwd(), 'backend', 'db_cred.py')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DB_SETTINGS'] = {}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_asc_to_csv(file_path):
    # Read the .asc file with the correct delimiter, handle quotes, and manage missing data
    df = pd.read_csv(file_path, delimiter=';', quotechar='"', header=0, na_values=[''])

    # Replace NaN values with empty strings to avoid issues with PostgreSQL
    df.fillna('', inplace=True)

    # Generate the output CSV file path
    csv_path = file_path.rsplit('.', 1)[0] + '.csv'

    # Save the DataFrame to a CSV file without the index column
    df.to_csv(csv_path, index=False)

    return csv_path


def update_db_cred_file(settings):
    with open(DB_CRED_FILE, 'w') as f:
        f.write(f"DB_HOST = '{settings['DB_HOST']}'\n")
        f.write(f"DB_PORT = '{settings['DB_PORT']}'\n")
        f.write(f"DB_NAME = '{settings['DB_NAME']}'\n")
        f.write(f"DB_USER = '{settings['DB_USER']}'\n")
        f.write(f"DB_PASSWORD = '{settings['DB_PASSWORD']}'\n\n")
        f.write(
            f"DATABASE_URL = f'postgresql://{settings['DB_USER']}:{settings['DB_PASSWORD']}@{settings['DB_HOST']}:{settings['DB_PORT']}/{settings['DB_NAME']}'\n")


@app.route('/upload_database', methods=['POST'])
def upload_database():
    if 'database' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('database')
    saved_files = []

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if filename.endswith('.asc'):
                converted_file = convert_asc_to_csv(file_path)
                saved_files.append(converted_file)
            else:
                saved_files.append(file_path)

            if filename.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    extract_folder = os.path.join(UPLOAD_FOLDER, filename[:-4])
                    os.makedirs(extract_folder, exist_ok=True)
                    zip_ref.extractall(extract_folder)
                    for root, dirs, files in os.walk(extract_folder):
                        for file in files:
                            saved_files.append(os.path.join(root, file))

        else:
            return jsonify({'error': f'File type not allowed: {file.filename}'}), 400

    app.config['UPLOADED_FILE_PATHS'] = saved_files

    return jsonify({'message': 'Files uploaded and converted successfully. Please update settings to import.'}), 200


@app.route('/update_settings', methods=['POST'])
def update_settings():
    settings = request.json
    required_fields = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']

    for field in required_fields:
        if not settings.get(field):
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        update_db_cred_file(settings)

        if 'UPLOADED_FILE_PATHS' in app.config:
            db_url = f"postgresql://{settings['DB_USER']}:{settings['DB_PASSWORD']}@{settings['DB_HOST']}:{settings['DB_PORT']}/{settings['DB_NAME']}"
            for file_path in app.config['UPLOADED_FILE_PATHS']:
                import_to_postgres(file_path, db_url)

            del app.config['UPLOADED_FILE_PATHS']
            return jsonify({'message': 'Settings updated and database imported successfully'}), 200
        else:
            return jsonify({'message': 'Settings updated successfully. No files to import.'}), 200
    except Exception as e:
        return jsonify({'error': f'Error updating settings or importing database: {str(e)}'}), 500


def import_to_postgres(file_path, db_url):
    print(f"Importing file to PostgreSQL: {file_path}")
    print(f"Database URL: {db_url}")
    os.environ["DATABASE_URL"] = str(db_url)
    upload_to_postgresql(file_path, db_url)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    history = data.get('history', [])
    # db_url = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"

    try:
        ai_response, response_type, response_data_explanation, query = sql_assistant(message)

        return jsonify({
            'data': ai_response,
            'type': response_type,
            'explanation': response_data_explanation,
            'query': query
        })
    except Exception as e:
        return jsonify({'error': f'Error processing chat: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
