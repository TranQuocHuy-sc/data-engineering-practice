import requests
import pandas as pd
from bs4 import BeautifulSoup


def main():
    url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    target_timestamp = "2024-01-19 10:27"
    file_to_download = None

    # Duyệt qua các hàng trong bảng
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            last_modified = cols[1].text.strip()
            if last_modified == target_timestamp:
                file_to_download = cols[0].find("a")["href"]
                break

    if not file_to_download:
        print("Không tìm thấy file phù hợp với timestamp.")
        return

    # Tải file
    download_url = url + file_to_download
    print(f"Đang tải: {download_url}")
    file_response = requests.get(download_url)
    file_response.raise_for_status()

    # Lưu file tạm
    with open("weather.csv", "wb") as f:
        f.write(file_response.content)

    # Đọc bằng pandas
    df = pd.read_csv("weather.csv")

    if "HourlyDryBulbTemperature" not in df.columns:
        print("Không tìm thấy cột 'HourlyDryBulbTemperature' trong dữ liệu.")
        return

    # Tìm giá trị lớn nhất của cột HourlyDryBulbTemperature
    max_temp = df["HourlyDryBulbTemperature"].max()
    hottest_records = df[df["HourlyDryBulbTemperature"] == max_temp]

    print("Bản ghi có nhiệt độ cao nhất:")
    print(hottest_records)


if __name__ == "__main__":
    main()
