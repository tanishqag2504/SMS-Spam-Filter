import streamlit as st
import pickle
import re
import string

with open("models/spam_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("models/vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()

    return text

st.set_page_config(
    page_title="SMS Spam Detector",
    page_icon="📱",
    layout="centered"
)


st.title("📱 SMS Spam Detector")
st.write("Enter an SMS message below to check whether it is **Spam** or **Not Spam**.")


message = st.text_area(
    "Enter your message:",
    placeholder="Example: Congratulations! You have won a free prize!"
)

if st.button("Check Message"):

    if message.strip() == "":
        st.warning("Please enter a message.")

    else:
        cleaned_message = clean_text(message)

        message_vector = vectorizer.transform([cleaned_message])

        prediction = model.predict(message_vector)[0]

        if prediction == 1:
            st.error("SPAM MESSAGE")
            st.write("This message has been classified as **Spam**.")

        else:
            st.success("NOT SPAM")
            st.write("This message appears to be **Not Spam**.")