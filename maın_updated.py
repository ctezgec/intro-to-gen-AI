
from openai import OpenAI
import streamlit as st

def get_env_value(key, filepath='.env'):
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):  # Skip comments/empty lines
                k, v = line.strip().split('=', 1)  # Split on first '=' only
                if k == key:
                    return v
    raise ValueError(f"Key '{key}' not found in {filepath}")


def generate(user_input:str, client, model="gpt-4.1-nano")->str:
    llm_output = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_input}],
        stream=True  
    )
    print(type(llm_output))
    return llm_output

# Modify the main function to include the streamlit app, 
# and connect it to the OpenAI API.
def main()->None:
    api_key = get_env_value('API_KEY')
    client = OpenAI(api_key=api_key)
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4.1-nano"
    # Add chat memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("How can I help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = generate(prompt, client=client, model=st.session_state["openai_model"])
            
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()