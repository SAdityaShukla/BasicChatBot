import os
from dotenv import load_dotenv
load_dotenv()


import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the question asked"),
        ("user","Question:{question}")
    ]
)


def generate_response(question,api_key,llm,temprature,max_tokens):
    groq_api_key = api_key
    llm = ChatGroq(model = llm,groq_api_key=groq_api_key)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({"question":question})
    return answer


## App Title
st.title("Enhanced Q&A Chatbot with GROQ")

## Sidebar for Settings
st.sidebar.title('Settings')
api_key = st.sidebar.text_input("Enter your groq API Key",type='password')


## DropDown to select various llm models
llm = st.sidebar.selectbox("Select your llm model",["llama-3.3-70b-versatile","llama-guard-4-12b","gemma2-9b-it"])

## Adjust Response Parameter
temprature = st.sidebar.slider("Temprature",min_value=0.0,max_value=1.0,value = 0.5)
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value = 150)

## Main interface for user input
st.write("What's on your mind today")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,api_key,llm,temprature,max_tokens)
    st.write(response)
else:
    st.write("Please enter a query.")