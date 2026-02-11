from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return  {"message": "NEXUS IS LIVE!"}

@app.post("/webhook")
async def receive_webhook(payload: dict):
    print("DING DONG! Someone is at the repo.")
    print(payload)
    return {"status": "ok"}