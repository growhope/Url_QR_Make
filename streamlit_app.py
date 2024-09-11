import streamlit as st
import pyshorteners
import qrcode
from PIL import Image
import io

def shorten_url(long_url):
    s = pyshorteners.Shortener()
    try:
        short_url = s.tinyurl.short(long_url)  # TinyURL을 사용하여 단축
        return short_url
    except Exception as e:
        st.error(f"URL을 단축하는 데 문제가 발생했습니다: {e}")
        return None

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    return img

def main():
    st.title("URL 단축기 및 QR 코드 생성기")

    # 사용자 입력 받기
    long_url = st.text_input("단축할 URL을 입력하세요:")

    if st.button("단축하기"):
        if long_url:
            short_url = shorten_url(long_url)
            if short_url:
                st.write(f"단축된 URL: [링크]({short_url})")
                
                # QR 코드 생성 및 표시
                qr_img = generate_qr_code(short_url)
                buffered = io.BytesIO()
                qr_img.save(buffered, format="PNG")
                qr_code_img = Image.open(io.BytesIO(buffered.getvalue()))
                
                st.image(qr_code_img, caption="단축된 URL의 QR 코드", use_column_width=True)
        else:
            st.warning("URL을 입력하세요.")

if __name__ == "__main__":
    main()
