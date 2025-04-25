import psycopg2
import csv


def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )


def execute_sql_file(filepath):
    with open(filepath, "r") as file:
        sql = file.read()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def clear_all_tables():
    conn = get_connection()
    cur = conn.cursor()

    print("Xóa dữ liệu cũ...")
    cur.execute("DELETE FROM transactions")
    cur.execute("DELETE FROM products")
    cur.execute("DELETE FROM accounts")

    conn.commit()
    cur.close()
    conn.close()


def insert_csv_to_table(csv_path, table_name, columns):
    conn = get_connection()
    cur = conn.cursor()

    with open(csv_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Bỏ qua header
        for row in reader:
            cur.execute(
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(row))})",
                row
            )

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("Đang tạo bảng...")
    execute_sql_file("create_tables.sql")

    print("Đang xóa dữ liệu cũ...")
    clear_all_tables()

    print("Đang insert dữ liệu từ CSV...")

    insert_csv_to_table("data/accounts.csv", "accounts",
                        ["customer_id", "first_name", "last_name", "address_1", "address_2", "city", "state", "zip_code", "join_date"])

    insert_csv_to_table("data/products.csv", "products",
                        ["product_id", "product_code", "product_description"])

    insert_csv_to_table("data/transactions.csv", "transactions",
                        ["transaction_id", "transaction_date", "product_id", "product_code", "product_description", "quantity", "account_id"])

    print("Đã hoàn thành thành công!")


if __name__ == "__main__":
    main()
