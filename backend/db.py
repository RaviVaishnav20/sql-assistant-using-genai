import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
import pandas as pd
from flask import jsonify
class PostgresManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def connect_with_url(self, url):
        self.connection = psycopg2.connect(url)
        self.cursor = self.connection.cursor()

    def upsert(self, table_name, _dict):
        columns = _dict.keys()
        values = [str(_dict[col]) if isinstance(_dict[col], int) else f"'{_dict[col]}'" for col in columns]
        update_values = [f"{col} = EXCLUDED.{col}" for col in columns]

        query = sql.SQL("""
            INSERT INTO {table} ({fields})
            VALUES ({values})
            ON CONFLICT (id)
            DO UPDATE SET {updates};
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(map(sql.Literal, values)),
            updates=sql.SQL(', ').join(map(sql.SQL, update_values))
        )

        self.cursor.execute(query)
        self.connection.commit()

    def delete(self, table_name, _id):
        query = sql.SQL("DELETE FROM {table} WHERE id = {id}").format(
            table=sql.Identifier(table_name),
            id=sql.Literal(_id)
        )

        self.cursor.execute(query)
        self.connection.commit()

    def get(self, table_name, _id):
        query = sql.SQL("SELECT * FROM {table} WHERE id = {id}").format(
            table=sql.Identifier(table_name),
            id=sql.Literal(_id)
        )

        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_all(self, table_name):
        query = sql.SQL("SELECT * FROM {table}").format(
            table=sql.Identifier(table_name)
        )

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def run_sql(self, sql_query):
        self.cursor.execute(sql_query)
        self.connection.commit()

        if sql_query.strip().lower().startswith("select"):
            # Fetch all rows from the executed SELECT query
            rows = self.cursor.fetchall()
            # Get column names
            columns = [desc[0] for desc in self.cursor.description]
            # Convert to DataFrame using a separate function
            df = self.convert_to_dataframe(rows, columns)
            return df, "HTML"

        else:
            # Return a confirmation message for non-SELECT queries
            return f"Query executed successfully: {sql_query}", "TEXT"

    def convert_to_dataframe(self, rows, columns):
        # Convert rows and columns to a DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Convert DataFrame to JSON
        # df_json = df.to_json(orient='records')

        # return jsonify(df_json)
        return df.to_html()


    # def run_sql(self, sql_query):
    #     self.cursor.execute(sql_query)
    #     self.connection.commit()

    def get_table_definitions(self, table_name):
        query = sql.SQL("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_name = {table}
        """).format(
            table=sql.Literal(table_name)
        )

        self.cursor.execute(query)
        columns = self.cursor.fetchall()

        create_table_sql = f"CREATE TABLE {table_name} (\n"
        for column in columns:
            col_def = f"  {column[0]} {column[1]}"
            if column[2]:
                col_def += f"({column[2]})"
            if column[3] == "NO":
                col_def += " NOT NULL"
            col_def += ",\n"
            create_table_sql += col_def

        create_table_sql = create_table_sql.rstrip(",\n") + "\n);"
        return create_table_sql

    def get_all_table_names(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"

        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    def get_table_definitions_for_prompt(self):
        tables = self.get_all_table_names()
        definitions = ""
        for table in tables:
            definitions += self.get_table_definitions(table) + "\n\n"
        return definitions





    def get_table_definitions_for_prompt_MOCK(self):
        return """CREATE TABLE users (
id integer,
created timestamp without time zone,
updated timestamp without time zone,
authed boolean,
plan text,
name text,
email text
);

CREATE TABLE jobs (
id integer,
created timestamp without time zone,
updated timestamp without time zone,
parentuserid integer,
status text,
totaldurationms bigint
    );"""

    def get_table_definition_map_for_embeddings(self):
        table_names = self.get_all_table_names()
        definitions = {}
        for table_name in table_names:
            definitions[table_name] = self.get_table_definitions(table_name)
        return definitions