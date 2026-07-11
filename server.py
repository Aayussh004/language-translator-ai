from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()


groq_api_key=os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="Llama-3.1-8b-instant",groq_api_key=groq_api_key)

# now we need to create template
order_template = "Convert all the input message to {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", order_template),
        ("user", "{text}"),
    ]
)

# create parser
parser = StrOutputParser()

# create chain
chain = prompt_template | llm | parser

# create app of fastapi

app = FastAPI(
    title="Translator of language",
    version="1.0.0",
    description="This robot will translate input texts to another language",
)

# now add the routes

add_routes(
    app,
    chain,
    path='/chain'
)

# host 
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)

