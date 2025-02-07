import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import io


st.set_page_config(page_title=" Basic Image Filter App")


# App Title
st.title("Basic Image Filter App")
st.write("Upload an image to filter it")


is_image_edited = False

st.sidebar.header("Filter Options")

uploaded_image = st.file_uploader(label="Upload an image", type=['jpg', 'png', 'jpeg'])


if uploaded_image:
    # Load the image
    image = Image.open(uploaded_image)
    st.image(image=image, caption="original Image", use_column_width=True)

    # Filter Options
    options = ["None", "Grayscale", "Invert Colors", "Brightness Adjustment"]
    filter_options = st.sidebar.radio(label="Choose a filter to apply", options=options)


    # Grayscale
    if filter_options == "Grayscale":
        is_image_edited = True
        filtered_image = ImageOps.grayscale(image)
        st.image(filtered_image, caption="Grayscale Image", use_column_width=True)


    # Invert Colors
    elif filter_options == "Invert Colors":
        is_image_edited = True
        # filtered_image = ImageOps.invert(image)
        filtered_image = ImageOps.invert(
            ImageOps.autocontrast((image.convert("RGB")))
        )
        st.image(filtered_image, caption="Inverted Image", use_column_width=True)


    # Brightness Adjustment
    elif filter_options == "Brightness Adjustment":
        is_image_edited = True
        brightness = st.sidebar.slider(label="Adjust Brightness", min_value=0.5, max_value=2.0, value=1.0, step=0.01)
        enhancer = ImageEnhance.Brightness(image)
        filtered_image = enhancer.enhance(brightness)
        st.image(filtered_image, caption="Brightness Adjusted Image", use_column_width=True)

    
    # Download the edited image
    if is_image_edited:
        if st.button(label="Click to download filtered image"):
            img_byte_arr = io.BytesIO()
            filtered_image.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
            
            st.download_button(
                label="Download Image",
                data=img_byte_arr,
                file_name="filtered_image.png",
                mime="image/png"
            )

else:
    st.write("Upload an image to begin")