from openai import OpenAI
import streamlit as st
import pandas as pd
from adaptkeybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import numpy as np
import copy

model = SentenceTransformer('all-MiniLM-L6-v2')
keyword_model = KeyBERT(model='all-MiniLM-L6-v2')

def extract_keywords_custom(text):
    res = keyword_model.extract_keywords(text.lower(), keyphrase_ngram_range=(1, 2), stop_words=["businesses", "business", "your"], top_n=10)
    res = [i[0] for i in res]
    return res

@st.cache
def load_projects():
    with st.spinner(text="Warming up projects..."):
        df = pd.read_csv('projects.csv', delimiter="\t")
        df['keywords'] = df['TLDRs'].apply(extract_keywords_custom)
        return df

projects = load_projects()

def rank_projects(user_keywords, projects):
    user_keywords_combined = " ".join(user_keywords)
    user_embedding = model.encode(user_keywords_combined, convert_to_tensor=True)
    project_embeddings = []
    for keywords in projects['keywords']:
        project_keywords_combined = " ".join(keywords)
        project_embedding = model.encode(project_keywords_combined, convert_to_tensor=True)
        project_embeddings.append(project_embedding)
    similarities = [util.pytorch_cos_sim(user_embedding, proj_emb).item() for proj_emb in project_embeddings]
    names = projects['Projects'].tolist()
    urls = projects['URLs'].tolist()
    tldrs = projects["TLDRs"].tolist()
    combined_data = list(zip(projects['Projects'], projects['URLs'], tldrs, similarities))
    combined_data.sort(key=lambda x: x[3], reverse=True)
    sorted_names, sorted_urls, sorted_tldrs, sorted_scores = zip(*combined_data)
    return sorted_names, sorted_urls, sorted_scores, sorted_tldrs

st.title("Talk to my Projects")

st.sidebar.title("User Keywords and Project Ranking")

st.info("To keep this service free, you have a limit of 10 messages.")

client = OpenAI(api_key=st.secrets["TOGETHER_API_KEY"], base_url="https://api.together.xyz/v1",)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "meta-llama/Llama-3-70b-chat-hf"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Your name is \"ProjEx\" (short for \"Project Explorer\"). Make conversation sound natural, do not re-intro yourself, always say Aman has worked on or attribute to Aman. You're an LLM whose objective is to ingest the project (of Aman Priyanshu) TLDRs and make conversation with the user. Ensure all your responses are short and to the point (within 2 sentences and not more than 50 words), they should be easy going and simple to understand. Discuss both business perspective and academic perspective as required. Context about the main project owner: Aman Priyanshu is a Masters student at Carnegie Mellon University specializing in Privacy Engineering, with research interests in Privacy-Preserving Machine Learning, Explainable AI, Fairness, and AI for Social Good. He has been recognized as an AAAI Undergraduate Consortium Scholar (2023) for his contributions to Fairness and Privacy, and his experience includes internships, publications, and awards in machine intelligence and security, as well as a passion for applying his research to develop applications for social good through hackathons. Note: Be careful of algorithms you claim to be created as mine beyond given context. Stick strongly to my projects given in the context below!"}]

for message in st.session_state.messages:
    if message["role"]=="system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        user_keywords = extract_keywords_custom(prompt)
        st.sidebar.write("User Keywords:", "`["+", ".join(user_keywords)+']`')
        sorted_names, sorted_urls, sorted_scores, sorted_tldrs = rank_projects(user_keywords, projects)
        if "context_tldrs" not in st.session_state:
            st.session_state.context_tldrs = copy.deepcopy(sorted_tldrs)
        else:
            st.session_state.context_tldrs = copy.deepcopy(sorted_tldrs)
        points = ""
        for i in range(len(sorted_names)):
            points += "* **"+sorted_names[i]+"** (_cosine:"+str(round(sorted_scores[i], 2))+"_)"+"\n   "+sorted_urls[i]+"\n"
        st.sidebar.markdown("## Top Projects:\n"+points)

    with st.chat_message("assistant"):
        if len(st.session_state.messages)<=10:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]+[{"role": "user", "content": "Most related projects:\n"+"\n".join([str(i+1)+". "+j for i,j in enumerate(st.session_state.context_tldrs[:3])])}],
                stream=True,
                temperature=0,

            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
    if len(st.session_state.messages)>10:
        st.warning("You've used your 10 free messages. To keep this service free, please use it sparingly. If you'd like to continue the conversation, feel free to reach out to me via \"amanpriyanshusms2001@gmail.com\"!")