import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",       # hoặc 127.0.0.1
            user="root",            # tên tài khoản MySQL
            password="123456",
            database="thoitiet"
        )
        if conn.is_connected():
            print("✅ Kết nối MySQL thành công")
            return conn
    except Error as e:
        print("❌ Lỗi khi kết nối MySQL:", e)
        return None
def main():
    create_connection()
if __name__ == "__main__":
    main()