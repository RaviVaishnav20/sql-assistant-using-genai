from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the model and tokenizer
model_name = "omeryentur/phi-3-sql"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_sql(table_info, question):
    # Prepare the prompt
    prompt = f"""
<|system|>
{table_info}

<|user|>
{question}

<|sql|>
"""

    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    # Generate the output
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=200,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
        )

    # Decode and return the generated SQL
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_sql.split("<|sql|>")[-1].strip()

# Example usage
table_info = """
Table: employees
Columns: 
- id (INT)
- name (VARCHAR)
- department (VARCHAR)
- salary (DECIMAL)
"""

question = "What is the average salary of employees in the IT department?"

sql_query = generate_sql(table_info, question)
print("Generated SQL Query:")
print(sql_query)