import streamlit as st
from unidecode import unidecode

def process_names(input_text):
    names = [name.strip() for name in input_text.strip().split("\n") if name.strip()]
    if not names:
        return None, None

    separated_names = []
    for full_name in names:
        parts = full_name.split()
        if len(parts) == 1:
            separated_names.append(("", parts[0]))
        else:
            last_name = " ".join(parts[:-1])
            first_name = parts[-1]
            separated_names.append((last_name, first_name))

    # Sắp xếp không phân biệt dấu
    separated_names.sort(key=lambda x: (unidecode(x[1]).lower(), unidecode(x[0]).lower()))
    return names, separated_names

def generate_output(separated_names):
    output = "STT\tHọ\tTên\n"
    for i, (last_name, first_name) in enumerate(separated_names, start=1):
        output += f"{i}\t{last_name}\t{first_name}\n"
    return output

# Giao diện Streamlit
st.title("Quản lý danh sách họ tên")

# Nhập liệu
data = st.text_area("Nhập danh sách họ tên (mỗi tên trên một dòng):", height=200)

if st.button("Xử lý"):
    if not data.strip():
        st.warning("Danh sách không hợp lệ hoặc trống!")
    else:
        _, separated_names = process_names(data)
        if separated_names:
            st.success("Xử lý thành công!")

            # Hiển thị kết quả trong bảng
            st.table({
                "STT": [i + 1 for i in range(len(separated_names))],
                "Họ": [name[0] for name in separated_names],
                "Tên": [name[1] for name in separated_names]
            })

            # Tải xuống kết quả
            output_text = generate_output(separated_names)
            st.download_button(
                label="Tải xuống kết quả",
                data=output_text,
                file_name="sorted_names.txt",
                mime="text/plain"
            )

            # Hiển thị kết quả để sao chép thủ công
            st.text_area("Kết quả đã xử lý (sao chép thủ công):", value=output_text, height=200)
