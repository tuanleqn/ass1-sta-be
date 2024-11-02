import os
from factory import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 10000))  # Lấy cổng từ biến môi trường, mặc định là 10000 nếu không có
    app.run(host="0.0.0.0", port=port)