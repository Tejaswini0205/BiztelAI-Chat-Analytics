from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os
from dotenv import load_dotenv
import openai  # ✅ Fix import
import asyncio  # ✅ Added async support

# ✅ Load environment variables
load_dotenv()

# ✅ Check API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ OpenAI API Key NOT found! Check your .env file.")
else:
    print("✅ OpenAI API Key Loaded.")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Path to dataset
DATA_PATH = "data/BiztelAI_DS_Dataset_Mar'25.json"

# ✅ Load dataset with error handling
try:
    df = pd.read_json(DATA_PATH).T  # Transpose for correct format
    df.reset_index(inplace=True)
    df.rename(columns={"index": "transcript_id"}, inplace=True)
    df.set_index("transcript_id", inplace=True)
    print("✅ Dataset loaded successfully!")
except Exception as e:
    print(f"❌ Error loading dataset: {str(e)}")
    df = pd.DataFrame()  # ✅ Prevent app crash


# ✅ Request Model for API
class TranscriptRequest(BaseModel):
    transcript_id: str


@app.get("/")
async def home():
    """Health check endpoint."""
    return {"message": "BiztelAI API is running"}


@app.get("/debug-transcripts")
async def debug_transcripts():
    """Check transcript structure."""
    return {
        "first_5_transcripts": list(df.index[:5]),
        "columns": list(df.columns)
    }


@app.get("/dataset-summary")
async def dataset_summary():
    """Returns summary of dataset."""
    try:
        unique_agents = set()
        for chat in df["content"]:
            if isinstance(chat, list):
                unique_agents.update(msg.get("agent", "Unknown") for msg in chat)

        return {
            "total_transcripts": df.shape[0],
            "unique_agents_count": len(unique_agents),
            "unique_agents": list(unique_agents),
            "sample_transcripts": df.head(2).to_dict(orient="index")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-transcript")
async def analyze_transcript(request: TranscriptRequest):
    """
    Analyze a transcript:
    - Extract article URL
    - Count agent messages
    - Detect sentiments
    - Generate LLM summary
    """
    transcript_id = request.transcript_id
    if transcript_id not in df.index:
        raise HTTPException(status_code=404, detail=f"Transcript ID {transcript_id} not found")

    transcript_data = df.loc[transcript_id]

    # ✅ Extract values safely
    article_url = transcript_data.get("article_url", "Unknown")
    content = transcript_data.get("content", [])
    if not isinstance(content, list):
        content = []

    # ✅ Count messages per agent
    agent_1_messages = sum(1 for msg in content if msg.get("agent") == "agent_1")
    agent_2_messages = sum(1 for msg in content if msg.get("agent") == "agent_2")

    # ✅ Extract sentiment ratings
    conversation_rating = transcript_data.get("conversation_rating", {})
    agent_1_sentiment = conversation_rating.get("agent_1", "Unknown")
    agent_2_sentiment = conversation_rating.get("agent_2", "Unknown")

    # ✅ Convert conversation to text format
    conversation_text = "\n".join([f"{msg['agent']}: {msg['message']}" for msg in content if "message" in msg])

    # ✅ Generate summary using OpenAI LLM (async)
    llm_summary = await generate_summary(conversation_text)

    return {
        "article_url": article_url,
        "agent_1_messages": agent_1_messages,
        "agent_2_messages": agent_2_messages,
        "agent_1_sentiment": agent_1_sentiment,
        "agent_2_sentiment": agent_2_sentiment,
        "summary": llm_summary
    }


# ✅ OpenAI GPT-4/GPT-3.5 LLM Summarization (async)
async def generate_summary(conversation_text: str) -> str:
    """Uses OpenAI API to generate a summary of the transcript asynchronously."""
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following conversation in 3-4 sentences."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI API Error: {e}"
