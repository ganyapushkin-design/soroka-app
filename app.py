import streamlit as st
import pandas as pd
import requests
from datetime import date

# --- НАСТРОЙКИ (Заполните свои данные) ---
TELEGRAM_TOKEN = "7548673060:AAFo133Yu4TmAIIDHhjwYGhyuPJ3-HxdIOQ"  # Получить у @BotFather
ADMIN_CHAT_ID = "264242317"      # Получить у @userinfobot
PAY_LINK = "https://yookassa.ru"   # Ссылка на вашу оплату
ADMIN_PASS = "soroka16"            # Пароль для входа в статистику

# Цены на события
PRICES = {
    "Мастер-класс по коллажу": 1200,
    "Лекция об искусстве": 600,
    "Киновечер в Сороке": 400
}

def send_tg_notification(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": ADMIN_CHAT_ID, "text": text, "parse_mode": "HTML"})
    except:
        pass

# --- ДИЗАЙН ---
st.set_page_config(page_title="Сорока Арт", page_icon="🐦")

# Меню
menu = st.sidebar.radio("Разделы", ["Главная", "Запись и Оплата", "Маркет", "Админка"])

if menu == "Главная":
    st.title("🐦 Арт-пространство «СОРОКА»")
    st.image("https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=1000")
    st.markdown("""
    **Кострома, ул. Горная, 16**
    
    Мы объединяем историю старинного особняка и современное искусство. 
    Приходите за вдохновением!
    """)

elif menu == "Запись и Оплата":
    st.header("Забронировать место")
    with st.form("book_form"):
        name = st.text_input("Ваше имя")
        phone = st.text_input("Телефон")
        event = st.selectbox("Выберите событие", list(PRICES.keys()))
        if st.form_submit_button("Записаться"):
            if name and phone:
                price = PRICES[event]
                # Сохраняем запись в память приложения
                if 'records' not in st.session_state: st.session_state.records = []
                st.session_state.records.append({"Дата": date.today(), "Имя": name, "Событие": event, "Сумма": price})
                
                # Сообщение владельцу
                send_tg_notification(f"💰 **Новая запись!**\n{name} ({phone})\n{event}\nК оплате: {price}₽")
                
                st.success(f"Заявка принята! К оплате {price}₽. Нажмите кнопку ниже для подтверждения.")
                st.link_button("💳 Оплатить билет", f"{PAY_LINK}")
            else:
                st.error("Пожалуйста, введите имя и телефон")

elif menu == "Маркет":
    st.header("Работы резидентов")
    st.write("Вы можете приобрести эти работы на Горной, 16")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=400")
        st.write("**Картина 'Волга'** — 5000₽")
    with col2:
        st.image("https://images.unsplash.com/photo-1582555172866-f73bb12a2ab3?q=80&w=400")
        st.write("**Скетч 'Старый город'** — 1500₽")

elif menu == "Админка":
    input_pass = st.text_input("Пароль администратора", type="password")
    if input_pass == ADMIN_PASS:
        st.subheader("Финансовый отчет")
        if 'records' in st.session_state and st.session_state.records:
            df = pd.DataFrame(st.session_state.records)
            st.metric("Общая выручка", f"{df['Сумма'].sum()} ₽")
            st.table(df)
        else:
            st.info("Записей пока нет")
