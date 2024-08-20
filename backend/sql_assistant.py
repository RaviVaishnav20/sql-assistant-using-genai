import os
from backend.db import PostgresManager
from backend import llm
import backend.db_cred as cfg
from backend import embeddings
DB_URL = cfg.DATABASE_URL


POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"
SQL_DELIMITER = "---------"

postgres_syntex_format = f"""
PostgreSQL syntax and execution:

Table Names and Quotation:

PostgreSQL uses double quotes for column names and table names if they have special characters, like periods (e.g., "card.csv"). However, it's better to avoid special characters in table names or quotes if not necessary. If the table names have periods, like "card.csv", ensure they are properly quoted.
PostgreSQL uses single quotes (') for string literals.
Aliasing Columns:

You should ensure that your table names/aliases are correct and consistent.
Count Function:

The COUNT(*) should count the number of loans per client, grouped by the client's client_id, issued, and loan status.
"""
def sql_assistant(message):
    prompt = f"Fulfill this database query: {message}."
    with PostgresManager() as db:
        # print("prompt v1", prompt)
        db.connect_with_url(DB_URL)
        map_table_name_to_table_def = db.get_table_definition_map_for_embeddings()

        database_embedder = embeddings.DatabaseEmbedder()

        for name, table_def in map_table_name_to_table_def.items():
            database_embedder.add_table(name, table_def)

        similar_tables = database_embedder.get_similar_tables(message, n=5)
        similar_tables = list(set(similar_tables))
        table_definitions = database_embedder.get_table_definitions_from_names(
            similar_tables
        )

        # table_definitions = db.get_table_definitions_for_prompt()

        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy the database query. Follow the postgrsql rules {postgres_syntex_format}. Before using any mathmatic operation or function check datatype if needed use cast. Ensure all columns are selected from the correct tables.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions,
        )
        # print("prompt v2", prompt)

        prompt = llm.add_cap_ref(
            prompt,
            f"\n\nDo not give any opening remarks or comments and also do not give any concluding remarks or comments. I need to be able to easily parse the sql query from your response. Give response in string",
            RESPONSE_FORMAT_CAP_REF,
            f"""<explanation of the sql query>
{SQL_DELIMITER}
<sql query exclusively as raw text>""",
        )

        # print("\n\n-------- PROMPT --------")
        # print(prompt)

        prompt_response = llm.prompt(
            f"Clean and format the following SQL query to ensure it is executable: {prompt} Ensure that the query adheres to SQL syntax standards, checks for potential issues, and confirms that the column and table names are accurate. Do not include any code block markers in the response.")
        # prompt_response = llm.prompt(prompt)
        # return prompt_response
        # print("\n\n-------- PROMPT RESPONSE --------")
        # print(prompt_response)

        sql_query = prompt_response.split(SQL_DELIMITER)[1].strip()
        explanation = prompt_response.split(SQL_DELIMITER)[0].strip()
        print(f"\n\n-------- PARSED SQL QUERY --------")
        print(sql_query)
        # print(type(sql_query))

        result = db.run_sql(sql_query)

        # print("\n\n======== POSTGRES DATA ANALYTICS AI AGENT RESPONSE ========")
        # print(result)

        return result[0], result[1], explanation+"----"+sql_query, sql_query


if __name__ == '__main__':
    message = "How many customers are available ?"
    for i in sql_assistant(message):
        print(i)
