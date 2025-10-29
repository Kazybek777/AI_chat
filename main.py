import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import streamlit as st
import json

# Скачиваем необходимые ресурсы NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Инициализируем компоненты NLP
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))

# Загружаем базу знаний
def load_data():
    try:
        with open('data/info_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Файл базы знаний не найден!")
        return {}

# Функция предобработки текста
def preprocess_text(text):
    # Токенизация
    tokens = word_tokenize(text.lower())
    # Удаление стоп-слов и лемматизация
    processed_tokens = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            lemma = lemmatizer.lemmatize(token)
            processed_tokens.append(lemma)
    return processed_tokens

def find_answer(question, knowledge_base):
    processed_question = preprocess_text(question)

    best_match = None
    max_score = 0

    # Ищем лучший match по категориям и подкатегориям
    for category, subcategories in knowledge_base.items():
        for subcategory, data in subcategories.items():
            keywords = data.get('keywords', [])
            # Считаем количество совпадений ключевых слов
            score = sum(1 for keyword in keywords if keyword in processed_question)

            if score > max_score:
                max_score = score
                best_match = data.get('response')

    return best_match if max_score > 0 else "Извините, я не понял ваш вопрос."

# Настройка Streamlit
st.set_page_config(page_title="Sagynbekovvv K", page_icon="😉")

st.title("Чат-бот")
st.markdown("")

knowledge_base = load_data()

prompt = st.text_input("Введите ваш вопрос:", placeholder="Например: Какие пары сегодня?")

if prompt:
    response = find_answer(prompt, knowledge_base)

    st.markdown("### Ответ:")
    st.info(response)

st.markdown("---")
st.markdown("Avtor: Sagynbekovvv K ❤️")