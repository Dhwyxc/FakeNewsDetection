import streamlit as st
import dill
import requests
import pandas as pd
import re
import time
import tensorflow as tf
from underthesea import word_tokenize
from keras.models import load_model
import pickle
from flask import Flask
#################################
# Các hàm tiền xử lý dữ liệu từ file notebook

with open("Data/vn-stopword.txt",encoding='utf-8') as file:
    stopwords = file.readlines()
    stopwords = [word.rstrip() for word in stopwords]

punctuations = '''!()-–=[]{}“”‘’;:'"|\,<>./?@#$%^&*_~'''

special_chars = ['\n', '\t']

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
        r'localhost|' # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ip
        r'(?::\d+)?' # port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def tokenize(text):
    tokenized_text = word_tokenize(text)
    return tokenized_text
def is_punctuation(token):
    global punctuations
    return True if token in punctuations else False
def is_special_chars(token):
    global special_chars
    return True if token in special_chars else False
def is_link(token):
    return re.match(regex, token) is not None
def lowercase(token):
    return token.lower()
def is_stopword(token):
    global stopwords
    return True if token in stopwords else False
def vietnamese_text_preprocessing(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if not is_punctuation(token)]
    tokens = [token for token in tokens if not is_special_chars(token)]
    tokens = [token for token in tokens if not is_link(token)]
    tokens = [lowercase(token) for token in tokens]
    tokens = [token for token in tokens if not is_stopword(token)]
    return tokens


###################################
# Hàm dự đoán
with open('Model/tokenizer.pkl', 'rb') as handle:
    tokenizer_saved = pickle.load(handle)
with open('Model/tfidf_vector.pkl', 'rb') as in_strm:
    saved_tfidf = dill.load(in_strm)
with open('Model/nb-model.pkl', 'rb') as in_strm:
    saved_nb = dill.load(in_strm)
with open('Model/tree-model.pkl', 'rb') as in_strm:
    saved_tree = dill.load(in_strm)
with open('Model/svc-model.pkl', 'rb') as in_strm:
    saved_svc = dill.load(in_strm)
model_rnn = load_model("Model/rnn-model_final.h5")

model_dict = {
        "Naive Bayes": "NB",
        "Decision Tree": "DT",
        "SVM": "SVM",
        "RNN": "RNN"
    }
################################################################
def model_predict(model, text):
    if (model == 'RNN'):
        print('RNNNNNNNNN')
        text = ' '.join(vietnamese_text_preprocessing(text))
        text = tokenizer_saved.texts_to_sequences([text])
        text = tf.keras.preprocessing.sequence.pad_sequences(text, padding='post', maxlen=256)
        pred_text = model_rnn.predict(text)[0][0]
        print(pred_text)
        if pred_text < 0.5:
            return 0
        else:
            return 1
    else:
        print("MLLLLLLLLLL")
        model_pd = ' '.join(vietnamese_text_preprocessing(text))
        tfid_text = saved_tfidf.transform([model_pd])
        if model == 'SVM':
            print("SVC")
            return saved_svc.predict(tfid_text)[0]
        elif model == 'NB':
            print("NB")
            return saved_nb.predict(tfid_text)[0]
        else:
            print("DT")
            return saved_tree.predict(tfid_text)[0]
###################################
# Tạo website đơn giản bằng streamlit

@st.cache(allow_output_mutation=True)
def load_session():
    return requests.Session()


def main():
    st.set_page_config(
        page_title="Fake news detection",
        page_icon=":newspaper:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title(":newspaper: FAKE NEWS DETECTION")
    sess = load_session()

    col1, col2 = st.columns([6, 4])
    with col2:
        st.image(f"visulize.png", width=700)

    with col1:
        model_name = st.selectbox("Choose model", index=0, options=list(model_dict.keys()))

        news = st.text_area("News to predict")
        entered_items = st.empty()

    button = st.button("Predict")

    st.markdown(
        "<hr />",
        unsafe_allow_html=True
    )

    if button:
        with st.spinner("Predicting..."):
            if not len(news):
                entered_items.markdown("In put at least a piece of news")
            else:
                print(model_name)
                model = model_dict[model_name]
                print("m",model)
                pred = model_predict(model, news)
                my_bar = st.progress(0)
                for p in range(100):
                    time.sleep(0.01)
                    my_bar.progress(p + 1)
                if pred == 0:
                    st.markdown("Non Fake news.")
                else:
                    st.markdown("Fake news!")

if __name__ == "__main__":
    main()

