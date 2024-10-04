import streamlit as st
import pandas as pd
# streamlit run app2.py

# Функція для завантаження файлу
def load_data():
    uploaded_file = st.file_uploader("Завантажте Excel файл", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    return None

# Головна частина програми
st.title("Візуалізація даних з Excel")

# Завантаження даних
data = load_data()

if data is not None:
    st.write("Дані з файлу:")
    st.dataframe(data)

    # Вибір стовпця для пошуку значення
    column = st.selectbox("Оберіть стовпчик для фільтрації:", data.columns)
    # Значення для фільтрації
    unique_values = data[column].unique()
    selected_value = st.selectbox("Оберіть значення для фільтрації:", unique_values)

    # Вибір стовпця дати
    # date_column = st.selectbox("Оберіть стовпчик дати:", data.columns)
    # data[date_column] = pd.to_datetime(data[date_column])  # Конвертація стовпця дати
    data['Date'] = pd.to_datetime(data['Date'])

    # Введення періоду
    start_date = st.date_input("Початкова дата", value=data['Date'].max().date())
    end_date = st.date_input("Кінцева дата", value=data['Date'].max().date())

    # Фільтрація даних за обраним значенням та датами
    filtered_data = data[
        (data[column] == selected_value) & 
        (data['Date'] >= pd.to_datetime(start_date)) & 
        (data['Date'] <= pd.to_datetime(end_date))
    ]

    st.write(filtered_data)

    # Побудова графіка
    st.subheader("Побудова графіка")
    
    if not filtered_data.empty:
        # Задання значень для осі X та Y
        x_column = filtered_data['Date']
        y_column = st.selectbox("Оберіть стовпчик для графіка:", data.columns)
        st.line_chart(filtered_data.set_index(x_column)[y_column])

#         if st.button("Побудувати графік"):
#             st.line_chart(filtered_data.set_index(x_column)[y_column])
#     else:
#         st.write("Немає даних за обраний період та значення.")
# else:
#     st.write("Завантажте Excel файл...")