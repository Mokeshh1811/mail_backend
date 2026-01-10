from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import smtplib
import ssl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
PORT = int(os.getenv("PORT", 3003))

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class EmailRequest(BaseModel):
    name: str
    email: EmailStr
    service: str
    message: str
    organization: str | None = None


def send_email(data: EmailRequest):
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = data.email
    msg["Subject"] = "Thank you for contacting Tempest!"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Thank you for contacting Tempest!</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #00AEC7, #0E4D8D);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .highlight {{
                color: #00AEC7;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 14px;
            }}
            .message-box {{
                background: white;
                border-left: 4px solid #00AEC7;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Thank You for Contacting Tempest!</h1>
            <p>We appreciate your interest in our services</p>
        </div>

        <div class="content">
            <p>Dear <strong>{data.name}</strong>,</p>

            <p>Thank you for reaching out to <span class="highlight">Tempest</span>! 
            We've received your inquiry about <strong>{data.service}</strong>.</p>

            {f"<p><strong>Organization:</strong> {data.organization}</p>" if data.organization else ""}

            <div class="message-box">
                <strong>Your Message:</strong><br>
                {data.message}
            </div>

            <p>Our team will review your request and get back to you within 24 hours.</p>

            <p>Best regards,<br>
            <strong>The Tempest Team</strong><br>
            <span class="highlight">Empowering Institutions with AI Solutions</span></p>
        </div>

        <div class="footer">
            <p>This email was sent to {data.email} | © 2025 Tempest.</p>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)


# API Endpoint
@app.post("/api/send-email")
async def send_email_endpoint(data: EmailRequest):
    try:
        send_email(data)
        return {"message": "Email sent successfully!"}
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=500, detail="Failed to send email")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
