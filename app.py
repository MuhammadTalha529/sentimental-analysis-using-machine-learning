from textblob import TextBlob
import pandas as pd
import streamlit as st
import cleantext
import emoji

st.title("Sentiment Web Analyzer")
background_image = 'image.jpg'

st.image(background_image, use_container_width=True)

st.header("Now Scale Your Thoughts")

with st.expander("Analyze Your Text"):
    text = st.text_input("Text here:")

    if text:
        blob = TextBlob(text)
        p = round(blob.sentiment.polarity, 2)
        st.write('Polarity :', p)

        if p >= 0.1:
            st.write(emoji.emojize("Positive Speech :grinning_face_with_big_eyes:"))
        elif p == 0.0:
            st.write(emoji.emojize("Neutral Speech :zipper-mouth_face:"))
        else:
            st.write(emoji.emojize("Negative Speech :disappointed_face:"))

        st.write('Subjectivity', round(blob.sentiment.subjectivity, 2))

#     pre = st.text_input('Clean Your Text: ')

# if pre:
#     cleaned = cleantext.clean(
#         pre,
#         fix_unicode=True,
#         to_ascii=True,
#         lower=True,
#         no_line_breaks=True,
#         no_urls=True,
#         no_emails=True,
#         no_phone_numbers=True,
#         no_numbers=True,
#         no_digits=True,
#         no_currency_symbols=True,
#         no_punct=True
#     )

#     st.write(cleaned)

pre = st.text_input('Clean Your Text: ')
if pre:
    st.write(cleantext.clean(pre, clean_all= False, extra_spaces=True , stopwords=True ,lowercase=True ,numbers=True , punct=True))

with st.expander('Analyze Excel files'):
    st.write("_**Note**_ : Your file must contain the column Name 'tweets' that contain the text to be analyzed.")
    upl = st.file_uploader('Upload file')

    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity

    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'

    if upl:
        df = pd.read_excel(upl)   # ✅ FIXED (was read_excels)

        # Ensure correct column name
        if 'tweets' not in df.columns:
            st.error("Column 'tweets' not found in file")
        else:
            df['score'] = df['tweets'].apply(score)
            df['analysis'] = df['score'].apply(analyze)
            st.write(df.head(10))

            @st.cache_data   # ✅ UPDATED (st.cache deprecated)
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='sentiment.csv',
                mime='text/csv',
            )

st.write("\n" * 15)

# Divider
st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

# Footer

st.write("Copy© 2026 Muhammad Talha | Made by Muhammad Talha")

