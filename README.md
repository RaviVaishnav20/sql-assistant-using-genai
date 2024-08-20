# SQL Assistant

SQL Assistant is a web application that allows users to interact with databases using natural language queries. It consists of a Flask backend and a React frontend.

## Directory Structure
```
sql-assistant/
├── backend/
│   ├── config.py
│   ├── db.py
│   ├── db_cred.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── sql_assistant.py
│   └── upload_to_postgres.py
├── src/
│   ├── components/
│   │   ├── DatabaseUpload.js
│   │   └── Settings.js
│   ├── App.css
│   ├── App.js
│   └── index.js
├── app.py
├── package.json
└── README.md

```
## Requirements

### Backend
- Python 3.8+
- Flask
- psycopg2
- pandas
- SQLAlchemy
- scikit-learn
- transformers
- openai

### Frontend
- Node.js 14+
- React 18+
- Axios
- react-icons
- react-loader-spinner
- node-html-parser

## Installation

### Backend Setup

1. Navigate to the project root directory:
cd sql-assistant
2. Create a virtual environment:
python -m venv venv
3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required Python packages:
pip install flask psycopg2-binary pandas sqlalchemy scikit-learn transformers openai

5. Set up the database credentials:
- Open `backend/db_cred.py`
- Update the database connection details (host, port, name, user, password)

6. Set up the Azure OpenAI API credentials:
- Open `backend/config.py`
- Add your Azure OpenAI API key, version, and endpoint

### Frontend Setup

1. Make sure you have Node.js installed on your system.

2. Navigate to the project root directory:
cd sql-assistant

3. Install the required npm packages:
npm install

## Running the Application

1. Start the Flask backend:
- Ensure you're in the project root directory and your virtual environment is activated
- Run the following command:
  ```
  python app.py
  ```
- The backend should start running on `http://localhost:8000`

2. Start the React frontend:
- Open a new terminal window
- Navigate to the project root directory
- Run the following command:
  ```
  npm start
  ```
- The frontend should start running on `http://localhost:3000`

3. Open your web browser and go to `http://localhost:3000` to use the SQL Assistant application.

## Usage

1. When you first open the application, click the settings icon in the top right corner to configure your database connection.

2. In the settings modal:
- Select your database type (SQL or NoSQL)
- Enter your database connection details
- Optionally upload a database file (supported formats: .db, .sqlite, .csv, .xls, .xlsx, .json)
- Click "Update Settings" to save your configuration

3. Once your database is connected, you can start asking questions in natural language in the chat interface.

4. The AI will generate SQL queries based on your questions and execute them against your database.

5. Results will be displayed in the chat, and you can download them as CSV files if needed.

6. Use the "Clear Chat" button to start a new conversation.

## Troubleshooting

- If you encounter any issues with database connections, double-check your credentials in the settings.
- Make sure both the backend and frontend servers are running simultaneously.
- Check the console logs in your browser and the terminal running the backend for any error messages.

