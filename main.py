from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import jwt
import time

load_dotenv()

app = FastAPI()

class MeetingRequest(BaseModel):
    meetingId: str
    password: str = None
    name: str

@app.post("/join")
async def join_meeting(meeting_request: MeetingRequest):
    sdk_key = os.getenv("ZOOM_SDK_KEY")
    sdk_secret = os.getenv("ZOOM_SDK_SECRET")
    meeting_id = meeting_request.meetingId
    password = meeting_request.password
    user_name = meeting_request.name

    # Generate a signature for the meeting
    token = generate_signature(meeting_id)
    
    # Here, you should implement logic to get a ZAK token if needed
    zak_token = "YOUR_ZAK_TOKEN"

    return {
        "sdkKey": sdk_key,
        "signature": token,
        "zakToken": zak_token,
    }

def generate_signature(meeting_id):
    # Generate a JWT token for Zoom meeting authentication
    payload = {
        "appKey": os.getenv("ZOOM_SDK_KEY"),
        "iat": int(time.time()),
        "exp": int(time.time()) + 5000,
        "meetingNumber": meeting_id,
        "role": 1,  # 1 for attendee
    }
    token = jwt.encode(payload, os.getenv("ZOOM_SDK_SECRET"), algorithm="HS256")
    return token

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)