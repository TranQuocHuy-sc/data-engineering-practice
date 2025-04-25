# Sử dụng image Python chính thức phiên bản 3.9
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements vào container
COPY requirements.txt .

# Cài đặt các phụ thuộc Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Thiết lập lệnh mặc định khi chạy container
CMD ["python", "main.py"]
