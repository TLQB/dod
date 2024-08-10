# import os
# import psycopg2

# # Lấy DATABASE_URL từ biến môi trường
# DATABASE_URL = os.environ.get('DATABASE_URL')

# # Kết nối tới cơ sở dữ liệu
# conn = psycopg2.connect(DATABASE_URL)
# cur = conn.cursor()

# # Đọc và thực thi các lệnh trong tệp init.sql
# with open('init.sql', 'r') as f:
#     cur.execute(f.read())

# # Đóng kết nối
# conn.commit()
# cur.close()
# conn.close()
