📘 Study Bot – AI Powered Study Assistant

Study Bot is an AI-powered chatbot designed to help students with academic and learning-related questions.
It supports context-aware conversations by storing chat history in MongoDB and is deployed as a FastAPI-based REST API with a modern web interface.

⸻

🚀 Features
	•	💬 AI-powered study assistant using an LLM
	•	🧠 Context-aware responses using MongoDB memory
	•	👤 User-specific conversations using unique user IDs
	•	🌐 REST API built with FastAPI
	•	📄 Interactive API documentation (Swagger UI)
	•	🎨 Modern ChatGPT-style web interface
	•	☁️ Cloud deployment using Render

⸻

🛠️ Tech Stack
	•	Backend: FastAPI
	•	LLM Integration: LangChain + Groq API
	•	Database: MongoDB (Atlas / Local)
	•	Frontend: HTML, CSS, JavaScript
	•	Deployment: Render

⸻

📂 Project Structure

study-bot/
│
├── app.py
├── requirements.txt
├── static/
│   ├── index.html        # Chatbot UI
│   └── redirect.html     # Landing page
├── .gitignore
└── README.md


⸻

⚙️ Setup Instructions (Local)

1️⃣ Clone the Repository

git clone https://github.com/<your-username>/study-bot.git
cd study-bot


⸻

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


⸻

3️⃣ Install Dependencies

pip install -r requirements.txt


⸻

4️⃣ Set Environment Variables

Create a .env file (DO NOT push this to GitHub):

GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string


⸻

5️⃣ Run the Application

uvicorn app:app --reload


⸻

🌐 Application URLs (Local)
	•	Landing Page: http://127.0.0.1:8000
	•	Chatbot UI: http://127.0.0.1:8000/ui
	•	API Docs: http://127.0.0.1:8000/docs

⸻

🧠 How Memory Works
	•	Each user is assigned a unique user_id
	•	All user messages and bot responses are stored in MongoDB
	•	Previous conversations are retrieved and passed to the LLM
	•	This enables context-aware responses

⸻

☁️ Deployment

The application is deployed on Render.
	•	Environment variables are configured in Render dashboard
	•	MongoDB Atlas is used for cloud database storage
	•	FastAPI serves both API endpoints and frontend UI

🔗 Hosted API Link:
(Add your Render deployment URL here)

⸻

📸 Screenshots

Screenshots included in the project report:
	•	Chat interface
	•	Swagger API documentation
	•	MongoDB chat history

⸻

🏁 Conclusion

Study Bot demonstrates the implementation of a real-world AI chatbot with persistent memory, API deployment, and a responsive user interface.
This project helped in understanding backend development, database integration, LLM usage, and cloud deployment.

⸻
