from fastapi import FastAPI, Request, HTTPException
import json

app = FastAPI()

@app.post("/api/callback")
async def callback(request: Request):
    try:
        payload = await request.json()

        if payload.get("code") != 200:
            raise HTTPException(status_code=400, detail="Task failed")

        data = payload.get("data", {})
        task_id = data.get("taskId")
        state = data.get("state")

        result_json = data.get("resultJson")
        if isinstance(result_json, str):
            result_json = json.loads(result_json)

        result_urls = result_json.get("resultUrls", [])

        print("Task ID:", task_id)
        print("State:", state)
        print("Result URLs:", result_urls)

        return {
            "status": "received",
            "taskId": task_id
        }

    except Exception as e:
        print("Callback error:", str(e))
        raise HTTPException(status_code=500, detail="Callback processing failed")
