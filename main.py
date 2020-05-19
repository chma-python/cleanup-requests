import os
from fastapi import FastAPI, Form, Response, Request, HTTPException
from slackers.server import router
from slackers.hooks import events
import logging
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator 
import time
import hmac
import hashlib
import binascii

app = FastAPI()
app.include_router(router)

log = logging.getLogger(__name__)

# token: xoxb-1134762843828-1125037727430-YczAdMzPuviJspRA4jY2kuw2

@events.on("message.channels")
def handle_mention(payload):
    log.info("message was posted")
    log.debug(payload)



@events.post("/nothook")
async def chat(
    request: Request, From: str = Form(...), Body: str = Form(...) 
):
    validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
    form_ = await request.form()
    if not validator.validate(
        str(request.url), 
        form_, 
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=400, detail="Error in Twilio Signature")

    response = MessagingResponse()
    msg = response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")

# async def chat(
#     request: Request, From: str = Form(...), Body: str = Form(...) 
# ):
#     validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])
#     form_ = await request.form()
#     if not validator.validate(
#         str(request.url), 
#         form_, 
#         request.headers.get("X-Twilio-Signature", "")
#     ):
#         raise HTTPException(status_code=400, detail="Error in Twilio Signature")

#     response = MessagingResponse()
#     msg = response.message(f"Hi {From}, you said: {Body}")
#     return Response(content=str(response), media_type="application/xml")

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}