import os
from factory import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)