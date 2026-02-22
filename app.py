import os
from click import prompt
from dotenv import load_dotenv
from langchain_core.runnables import chain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
mongo_uri = os.getenv("MONGODB_URI")


client = MongoClient(mongo_uri)
db = client["chatBot"]
collection = db["users"]

app = FastAPI()

app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

class ChatRequest(BaseModel):
    user_id: str
    question: str
    

#allow all ip addresses to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Study Bot — a concise, helpful AI assistant for academic and learning-related questions.\n"
            "Rules:\n"
            "- Give clear, accurate, and to-the-point answers.\n"
            "- Keep responses short by default (3–6 sentences).\n"
            "- Only give long explanations if the user explicitly asks for detailed or step-by-step answers.\n"
            "- Use simple language suitable for students.\n"
            "- Use bullet points or short examples when helpful.\n"
            "- Answer only study or education-related questions.\n"
            "- Use conversation history only when relevant.\n"
            "- Do not add unnecessary filler text."
        ),
        ("placeholder", "{history}"),
        ("user", "{question}")
    ]
)


llm = ChatGroq(api_key=groq_api_key, model="openai/gpt-oss-120b")
chain = prompt | llm

# user_id = "user987"

def get_chat_history(user_id):
    history = collection.find({"user_id": user_id}).sort("timestamp", 1)
    return [{"role": entry["role"], "content": entry["message"]} for entry in history]

@app.get("/", response_class=HTMLResponse) # Define a simple route to test the API    
def root():
    return Path("static/redirect.html").read_text()


@app.post("/chat")
def chat(chat_request: ChatRequest):
    try:
        history = get_chat_history(chat_request.user_id)

        response = chain.invoke({
            "history": history,
            "question": chat_request.question
        })

        collection.insert_one({
            "user_id": chat_request.user_id,
            "role": "user",
            "timestamp": datetime.now(timezone.utc),
            "message": chat_request.question,
        })

        collection.insert_one({
            "user_id": chat_request.user_id,
            "role": "assistant",
            "timestamp": datetime.now(timezone.utc),
            "message": response.content,
        })

        return {
            "response": response.content
        }

    except Exception as e:
        print("BACKEND ERROR:", e)
        return {
            "error": "Something went wrong while generating response"
        }

# @app.post("/chat") # Define a route to handle chat requests
# def chat(chat_request: ChatRequest):
#     history = get_chat_history(chat_request.user_id)
#     response = chain.invoke({"history": history, "question": chat_request.question})
#     collection.insert_one(
#         {
#             "user_id": chat_request.user_id, 
#             "role": "user",
#             "timestamp": datetime.now(timezone.utc),
#             "message": chat_request.question, 
#         } 
#     )
#     collection.insert_one(
#         {
#             "user_id": chat_request.user_id, 
#             "role": "assistant",
#             "timestamp": datetime.now(timezone.utc),
#             "message": response.content, 
#         }
#     )
#     return {"response": response.content}



# while True:
#     question = input("Enter your question (or 'exit' to quit): ")
#     if question.lower() == "exit" or question.lower() == "quit":
#         break
#     response = chain.invoke({"history": get_chat_history(user_id), "question": question})
#     print("Response:", response.content)
#     collection.insert_one(
#         {
#             "user_id": user_id, 
#             "role": "user",
#             "timestamp": datetime.now(timezone.utc),
#             "message": question, 
#         }
#     ) 
#     collection.insert_one(
#         {
#             "user_id": user_id, 
#             "role": "assistant",
#             "timestamp": datetime.now(timezone.utc),
#             "message": response.content, 
#         }
#     ) 
# print("Chat ended. Goodbye!")