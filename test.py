import pandas as pd

# Tên tệp JSON đầu vào và tệp Excel đầu ra
JSON_FILE_PATH = 'Gift_Cards.json' 
OUTPUT_EXCEL_FILE = 'Du_lieu_GiftCards_Amazon.xlsx'

try:
    # 1. Đọc dữ liệu JSON Lines
    # Dữ liệu Amazon thường là JSON Lines (mỗi dòng là một đối tượng JSON)
    df = pd.read_json(JSON_FILE_PATH, lines=True)

    print(f"--- Đọc Dữ liệu {JSON_FILE_PATH} Thành công ---")
    print(f"Kích thước bộ dữ liệu thô: {df.shape[0]} hàng")
    
    # 2. Xử lý và Đổi tên cột Cốt lõi
    # Giữ lại và đổi tên các cột phổ biến trong dữ liệu Amazon Review
    df_processed = df.rename(columns={
        'reviewerID': 'username_ID',     # ID người dùng (thường không có tên thật)
        'asin': 'product_id',           # ID sản phẩm Amazon (ASIN)
        'overall': 'rating_star',       # Điểm đánh giá (1-5)
        'reviewText': 'comment',        # Nội dung bình luận
        'reviewTime': 'ctime',          # Thời gian đánh giá
        'price': 'price'                # Giá (nếu có trong file này)
    })
    
    # 3. Lọc và chuẩn bị các cột bạn cần
    # Lưu ý: Cột product_name và product_category thường phải JOIN từ file Metadata khác.
    required_cols = [
        'username_ID', 'rating_star', 'comment', 'price', 'ctime', 
        'product_id' # Giữ lại ID để có thể JOIN sau này
    ]
    
    # Lọc các cột có tồn tại trong DataFrame
    cols_to_keep = [col for col in required_cols if col in df_processed.columns]
    df_final = df_processed[cols_to_keep]

    # 4. Xuất sang tệp Excel (.xlsx)
    df_final.to_excel(
        OUTPUT_EXCEL_FILE, 
        index=False,               # Không ghi chỉ mục của DataFrame
        engine='openpyxl'
    )
    
    print("--- Xuất Dữ liệu sang Excel Hoàn tất ---")
    print(f"Dữ liệu đã được lưu vào tệp: {OUTPUT_EXCEL_FILE}")
    print(f"Số lượng bản ghi cuối cùng: {df_final.shape[0]}")
    print("\n5 Dòng Dữ liệu Mẫu (Đã được chuyển đổi):")
    print(df_final.head())

except FileNotFoundError:
    print(f"LỖI: Không tìm thấy tệp JSON tại đường dẫn: {JSON_FILE_PATH}. Vui lòng kiểm tra tên tệp.")
except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")