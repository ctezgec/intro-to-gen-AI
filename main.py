
from openai import OpenAI

def get_env_value(key, filepath='.env'):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):  # Skip comments/empty lines
                k, v = line.strip().split('=', 1)  # Split on first '=' only
                if k == key:
                    return v
    raise ValueError(f"Key '{key}' not found in {filepath}")

def generate(user_input:str, client, model="gpt-4.1-nano")->str:

    llm_output = client.responses.create(
        model=model,
        input = user_input
    )
    return llm_output


def main()->None:
    api_key = get_env_value('API_KEY')
    client = OpenAI(api_key=api_key)
    a = input("Enter your input: ")
    while True:
        if a == "/bye":
            break
        else:
            llm_output = generate(a, client=client)
            print(llm_output.output_text)
            a = input("Enter your input: ")

if __name__ == "__main__":
    main()