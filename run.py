import os
from app.twilio_webhook import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use 5000 locally, use $PORT on Render
    app.run(host='0.0.0.0', port=port, debug=True)
