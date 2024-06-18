import streamlit as st
import anthropic
import base64
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title='img2txt', page_icon='icons/Transformed image.webp',layout="wide",menu_items=None)

client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
st.header("img2txt")

image = st.file_uploader("Upload a image",type=['jpg','png','jpeg'],accept_multiple_files=False)
if image is not None:
    try:
        media_type=image.name.split('.')[-1]
        image_data=image.getvalue()
        image_media_type = f"image/{media_type}"
        image_data = base64.b64encode(image_data).decode()
        col1, col2 = st.columns(2)
        with col1:
            st.image(image)
        
        with client.messages.stream(
        max_tokens=1024,
        messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "First, a brief description of the image to be used as alt text. Do not describe or extract text in the description. Second, the text extracted from the image, with newlines where applicable. Un-obstruct text if it is covered by something, to make it readable. If there is no text in the image, only respond with the description. Do not include any other information and do not add any formattings.",
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": image_media_type,
                                "data":image_data,
                            },
                        },
                    ],
                }
            ],
        model="claude-3-haiku-20240307",
        ) as stream:
            with col2:
                st.write_stream(stream.text_stream)
    except Exception as e:
          st.write(f"Unable to process the image {e}")