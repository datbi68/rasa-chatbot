from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Dữ liệu từ Rasa domain.yml
responses = {
    'thong_tin_can_bo': "Các cán bộ, giảng viên được đào tạo tại các cơ sở uy tín trong nước và quốc tế gồm có 2 Phó giáo sư, 8 Tiến sĩ, 9 Thạc sĩ (4 Nghiên cứu sinh).",
    'co_so_vat_chat': "Khoa có 16 phòng máy, 2 phòng thí nghiệm chất lượng cao phục vụ cho công tác đào tạo và nghiên cứu khoa học.",
    'chuong_trinh_dao_tao': "Hệ thống đào tạo của Khoa bao gồm: 3 chương trình đào tạo Cử nhân, 2 chương trình đào tạo Thạc sĩ, 2 chương trình đào tạo Tiến sĩ.",
    'hoat_dong_sinh_vien': "Hàng năm, có nhiều hoạt động dành cho sinh viên, học viên: Hội nghị sinh viên nghiên cứu khoa học, tuần nghiệp vụ sư phạm, ...",
    'thong_tin_chung_khoa': "Khoa Công nghệ Thông tin tại Trường Đại học Sư phạm Hà Nội là một nơi năng động và sáng tạo. Chúng tôi tận tâm đào tạo và trang bị cho sinh viên kiến thức chuyên sâu về lĩnh vực Công nghệ Thông tin, từ phát triển ứng dụng đến quản lý hệ thống thông tin.",
    'thong_tin_tuyen_sinh': "Tổng chỉ tiêu tuyển sinh: 240\nChỉ tiêu tuyển sinh Ngành Sư phạm Tin học: 120\nChỉ tiêu tuyển sinh Ngành Công nghệ thông tin: 120\nĐiểm sàn: 21 đối với cả 2 ngành.",
    'diem_san_tuyen_sinh': "Điểm sàn năm 2024-2025 là 21 điểm.",
    'diem_trung_tuyen_nam': "Ngành Công nghệ thông tin:\n- Tổ hợp xét tuyển A00: 24.10 điểm\n- Tổ hợp xét tuyển A01: 24.10 điểm\nNgành Sư phạm Tin học:\n- Tổ hợp xét tuyển A00: 25.10 điểm\n- Tổ hợp xét tuyển A01: 25.10 điểm",
    'nganh_dao_tao': "Các ngành đào tạo của khoa bao gồm:\n- Công nghệ thông tin: Đào tạo các cử nhân về Công nghệ phần mềm và Khoa học dữ liệu.\n- Sư phạm Tin học: Đào tạo giáo viên Tin học các cấp.\n- Sư phạm Tin học dạy bằng Tiếng Anh.",
    'lich_su_diem_trung_tuyen': "Điểm trúng tuyển 3 năm gần đây:\nNăm 2023-2024: CNTT (A00: 23.7, A01: 23.56), SPTH (A00: 24.2, A01: 23.66)\nNăm 2022-2023: CNTT (A00: 23.9, A01: 23.85), SPTH (A00: 23.55, A01: 23.45)\nNăm 2021-2022: CNTT (A00: 22.15, A01: 21.8), SPTH (A00: 21.35, A01: 21)"
}

# Keywords từ Rasa NLU
keywords = {
    'thong_tin_can_bo': ['cán bộ', 'giảng viên', 'giáo viên', 'đội ngũ', 'tiến sĩ', 'thạc sĩ'],
    'co_so_vat_chat': ['cơ sở vật chất', 'phòng máy', 'phòng thí nghiệm', 'trang thiết bị'],
    'chuong_trinh_dao_tao': ['chương trình đào tạo', 'hệ thống đào tạo', 'thạc sĩ', 'tiến sĩ', 'cử nhân'],
    'hoat_dong_sinh_vien': ['hoạt động sinh viên', 'sự kiện', 'hội nghị', 'nghiên cứu khoa học'],
    'thong_tin_chung_khoa': ['giới thiệu', 'thông tin chung', 'khoa cntt', 'khoa công nghệ'],
    'thong_tin_tuyen_sinh': ['tuyển sinh', 'chỉ tiêu'],
    'diem_san_tuyen_sinh': ['điểm sàn', 'ngưỡng điểm'],
    'diem_trung_tuyen_nam': ['điểm trúng tuyển', 'điểm chuẩn', 'năm nay'],
    'nganh_dao_tao': ['ngành đào tạo', 'ngành học', 'sư phạm tin học', 'công nghệ thông tin'],
    'lich_su_diem_trung_tuyen': ['lịch sử điểm', 'điểm chuẩn 3 năm', 'qua các năm', '2021', '2022', '2023']
}

def detect_intent(message):
    message = message.lower()
    
    # Tính điểm cho mỗi intent
    scores = {}
    for intent, words in keywords.items():
        score = sum(1 for word in words if word in message)
        if score > 0:
            scores[intent] = score
    
    # Trả về intent có điểm cao nhất
    if scores:
        return max(scores, key=scores.get)
    return None

@app.route('/webhooks/rest/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get('message', '')
    
    intent = detect_intent(message)
    
    if intent and intent in responses:
        response_text = responses[intent]
    else:
        response_text = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi về: thông tin khoa, tuyển sinh, điểm chuẩn, cơ sở vật chất, cán bộ giảng viên, ngành đào tạo..."
    
    return jsonify([{"text": response_text}])

@app.route('/')
def home():
    return "Rasa Chatbot API is running!"

if __name__ == '__main__':
    app.run()
