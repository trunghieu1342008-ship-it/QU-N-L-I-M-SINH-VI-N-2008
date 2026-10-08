import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên - Lê Minh Tuấn",
    page_icon="🎓",
    layout="wide"
)

# 1. Hiển thị tiêu đề
st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# Tạo dữ liệu mẫu cho 10 sinh viên
@st.cache_data
def load_data():
    data = [
        {"Họ tên": "Nguyễn Văn An", "Chuyên cần": 8.5, "Giữa kỳ": 7.0, "Cuối kỳ": 8.0},
        {"Họ tên": "Trần Thị Bích", "Chuyên cần": 9.0, "Giữa kỳ": 8.5, "Cuối kỳ": 9.0},
        {"Họ tên": "Lê Hoàng Cường", "Chuyên cần": 7.0, "Giữa kỳ": 6.0, "Cuối kỳ": 5.5},
        {"Họ tên": "Phạm Thị Dung", "Chuyên cần": 10.0, "Giữa kỳ": 9.0, "Cuối kỳ": 9.5},
        {"Họ tên": "Hoàng Văn Đức", "Chuyên cần": 6.5, "Giữa kỳ": 5.0, "Cuối kỳ": 4.0},
        {"Họ tên": "Vũ Thị Hoa", "Chuyên cần": 8.0, "Giữa kỳ": 7.5, "Cuối kỳ": 7.0},
        {"Họ tên": "Đỗ Minh Hùng", "Chuyên cần": 9.0, "Giữa kỳ": 8.0, "Cuối kỳ": 8.5},
        {"Họ tên": "Bùi Thị Linh", "Chuyên cần": 7.5, "Giữa kỳ": 6.5, "Cuối kỳ": 6.0},
        {"Họ tên": "Ngô Quang Minh", "Chuyên cần": 8.5, "Giữa kỳ": 9.0, "Cuối kỳ": 8.0},
        {"Họ tên": "Dương Thùy Nga", "Chuyên cần": 9.5, "Giữa kỳ": 9.5, "Cuối kỳ": 9.0}
    ]
    df = pd.DataFrame(data)
    
    # Tính Tổng kết (Ví dụ: Chuyên cần * 10% + Giữa kỳ * 30% + Cuối kỳ * 60%)
    df["Tổng kết"] = round(df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6, 2)
    
    # Xếp loại và Đạt/Không đạt
    def get_rank(score):
        if score >= 8.5: return "Giỏi"
        elif score >= 7.0: return "Khá"
        elif score >= 5.0: return "Trung bình"
        else: return "Yếu"
        
    df["Xếp loại"] = df["Tổng kết"].apply(get_rank)
    return df

df_students = load_data()

# 2. Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng Điểm Chi Tiết Của Lớp")
st.dataframe(df_students, use_container_width=True)

st.markdown("---")

# Tính toán các chỉ số thống kê
avg_class = round(df_students["Tổng kết"].mean(), 2)
max_student = df_students.loc[df_students["Tổng kết"].idxmax()]
min_student = df_students.loc[df_students["Tổng kết"].idxmin()]
passed_count = len(df_students[df_students["Tổng kết"] >= 5.0])

# 3, 4, 5. Hiển thị điểm trung bình, cao nhất/thấp nhất, số sinh viên đạt
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 Điểm Trung Bình Cả Lớp", value=f"{avg_class} / 10")
with col2:
    st.metric(label="🏆 Điểm Tổng Kết Cao Nhất", value=f"{max_student['Tổng kết']} ({max_student['Họ tên']})")
with col3:
    st.metric(label="⚠️ Điểm Tổng Kết Thấp Nhất", value=f"{min_student['Tổng kết']} ({min_student['Họ tên']})")

col_extra1, _ = st.columns([1, 2])
with col_extra1:
    st.metric(label="✅ Số Sinh Viên Đạt (>= 5.0)", value=f"{passed_count} / {len(df_students)}")

st.markdown("---")

# 6 & 7. Tạo danh sách xổ xuống chọn sinh viên và xem thông tin chi tiết
st.subheader("🔍 Tra Cứu Thông Tin Sinh Viên")
selected_name = st.selectbox("Chọn sinh viên để xem chi tiết điểm:", df_students["Họ tên"].tolist())

# Lọc dữ liệu của sinh viên được chọn
student_info = df_students[df_students["Họ tên"] == selected_name].iloc[0]

sc1, sc2, sc3, sc4, sc5 = st.columns(5)
with sc1:
    st.metric("Chuyên cần", f"{student_info['Chuyên cần']}")
with sc2:
    st.metric("Giữa kỳ", f"{student_info['Giữa kỳ']}")
with sc3:
    st.metric("Cuối kỳ", f"{student_info['Cuối kỳ']}")
with sc4:
    st.metric("Tổng kết", f"{student_info['Tổng kết']}")
with sc5:
    st.metric("Xếp loại", f"{student_info['Xếp loại']}")

st.markdown("---")

# 8. Hiển thị biểu đồ cột điểm tổng kết của 10 sinh viên
st.subheader("📊 Biểu Đồ Cột Điểm Tổng Kết Của 10 Sinh Viên")
chart_data = df_students.set_index("Họ tên")[["Tổng kết"]]
st.bar_chart(chart_data)

st.markdown("---")

# 9. Hiển thị họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>"
    "Người tạo ứng dụng: Lê Minh Tuấn | MSSV: 051208004610"
    "</p>", 
    unsafe_allow_html=True
)
