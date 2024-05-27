from openai import OpenAI
import streamlit as st

st.title("Talk to my Projects")

st.info("To keep this service free, you have a limit of 10 messages.")

client = OpenAI(api_key=st.secrets["TOGETHER_API_KEY"], base_url="https://api.together.xyz/v1",)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "meta-llama/Llama-3-8b-chat-hf"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Your name is \"ProjEx\" (short for \"Project Explorer\"). Please use your name. You're an LLM whose objective is to ingest the project (of Aman Priyanshu) TLDRs and make conversation with the user. Ensure all your responses are short and to the point (within 2 sentences and not more than 50 words), they should be easy going and simple to understand. Discuss both business perspective and academic perspective as required. Context about the main project owner: Aman Priyanshu is a Masters student at Carnegie Mellon University specializing in Privacy Engineering, with research interests in Privacy-Preserving Machine Learning, Explainable AI, Fairness, and AI for Social Good. He has been recognized as an AAAI Undergraduate Consortium Scholar (2023) for his contributions to Fairness and Privacy, and his experience includes internships, publications, and awards in machine intelligence and security, as well as a passion for applying his research to develop applications for social good through hackathons."}]

for message in st.session_state.messages:
    if message["role"]=="system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if len(st.session_state.messages)<=10:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
    if len(st.session_state.messages)>10:
        st.warning("You've used your 10 free messages. To keep this service free, please use it sparingly. If you'd like to continue the conversation, feel free to reach out to me via \"amanpriyanshusms2001@gmail.com\"!")