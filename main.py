from flask import Flask, request, jsonify
from flask_cors import CORS
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

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def send_email(data):
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = data["email"]
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
            <p>Dear <strong>{data["name"]}</strong>,</p>

            <p>Thank you for reaching out to <span class="highlight">Tempest</span>! 
            We've received your inquiry about <strong>{data["service"]}</strong>.</p>

            {f"<p><strong>Organization:</strong> {data.get('organization')}</p>" if data.get("organization") else ""}

            <div class="message-box">
                <strong>Your Message:</strong><br>
                {data["message"]}
            </div>

            <p>Our team will review your request and get back to you within 24 hours.</p>

            <p>Best regards,<br>
            <strong>The Tempest Team</strong><br>
            <span class="highlight">Empowering Institutions with AI Solutions</span></p>
        </div>

        <div class="footer">
            <p>This email was sent to {data["email"]} | © 2025 Tempest.</p>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)


@app.route("/api/send-email", methods=["POST"])
def send_email_api():
    try:
        data = request.get_json()

        required_fields = ["name", "email", "service", "message"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        send_email(data)
        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"error": "Failed to send email"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
