import psycopg2
import csv

def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )

def execute_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        sql = f.read()
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def insert_csv_to_table(csv_path, table_name, columns):
    conn = get_connection()
    cur = conn.cursor()
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            cur.execute(
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(row))})",
                row
            )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Đã insert dữ liệu vào bảng `{table_name}` từ `{csv_path}`")

def main():
    print("Đang tạo bảng...")
    execute_sql_file("create_tables.sql")

    print("Đang insert dữ liệu từ CSV...")
    insert_csv_to_table("data/accounts.csv", "accounts",
                        ["customer_id", "first_name", "last_name", "address_1", "address_2", "city", "state", "zip_code", "join_date"])
    insert_csv_to_table("data/products.csv", "products",
                        ["product_id", "product_code", "product_description"])
    insert_csv_to_table("data/transactions.csv", "transactions",
                        ["transaction_id", "transaction_date", "product_id", "product_code", "product_description", "quantity", "account_id"])

    print("🎉 Tất cả dữ liệu đã được chèn thành công!")

if __name__ == "__main__":
    main()
