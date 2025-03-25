 # BiztelAI Chat Analytics

BiztelAI Chat Analytics is an AI-driven analytics system designed to process and analyze chat transcripts. The system extracts insights, performs sentiment analysis, and provides a REST API for querying analytics.

## 🚀 Features
- 📂 **Data Ingestion**: Supports structured chat transcripts for analysis.
- 🔍 **Exploratory Data Analysis (EDA)**: Generates statistical insights on chat data.
- 😊 **Sentiment Analysis**: Classifies messages into positive, negative, or neutral.
- 🏗️ **RAG-Based QA System**: Uses Retrieval-Augmented Generation (RAG) for answering questions from chat history.
- 📊 **Analytics API**: Exposes insights via a REST API built using FastAPI.
- 📸 **Automated Visualizations**: Generates and stores insightful plots from chat analytics.
- ⚡ **Optimized Performance**: Supports parallel processing for faster results.
- 🐳 **Dockerization** *(Optional)*: Can be deployed as a containerized service.


## 📊 Generated Plots
The system generates various visualizations and stores them in the **`plots/`** folder:
- **sentiment_distribution.png** → Sentiment breakdown of messages.
- **message_trends.png** → Trends in chat volume over time.
- **response_times.png** → Analysis of agent response times.

These plots help in understanding chat behaviors and trends over time.

## 🛠️ Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/Tejaswini0205/BiztelAI-Chat-Analytics.git
   cd BiztelAI-Chat-Analytics
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
3. Install Dependencies
pip install -r requirements.txt
4. Run the API
uvicorn backend.api.main:app --reload

📡 API Endpoints
Method	Endpoint	Description
GET	/analytics	Fetch chat analytics
POST	/query	Ask a question (RAG-based)
POST	/sentiment	Perform sentiment analysis

🤖 Technologies Used
FastAPI - For building the REST API.
Pandas - Data preprocessing.
NLTK & Transformers - Sentiment analysis.
FAISS - Vector search for RAG.
Matplotlib & Seaborn - Plot generation.
OpenAI API (optional) - LLM-based analytics.

📜 License
This project is licensed under the MIT License.
