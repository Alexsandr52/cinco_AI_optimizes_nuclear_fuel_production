import re
import json
import streamlit as st
import pandas as pd
from back import main


# нормализуем таблицу. удаляем строки с n/a, соединяем значения этих строк со значениями ячеек над ними
def correct_table(data_frame: pd.DataFrame):
    for i in range(0, len(data_frame), 2):
        for col in data_frame.columns:
            if pd.notnull(data_frame.loc[i, col]) and pd.notnull(data_frame.loc[i + 1, col]):
                data_frame.loc[i, col] += ' ' + data_frame.loc[i + 1, col]
            elif pd.isnull(data_frame.loc[i, col]) and pd.notnull(data_frame.loc[i + 1, col]):
                data_frame.loc[i, col] = data_frame.loc[i + 1, col]
    return data_frame[data_frame['Сплав'].notna()]


def transform_field(value, field_name):
    if isinstance(value, str):
        match1 = re.match(
            r'(\d+)-(\d+)х?(\d*) (\d+),?(\d*)ч\+(\d+)м (\w+)', value)
        match2 = re.match(r'(\d+)ч (\w+)', value)
        if match1:
            hours = int(match1.group(4))
            minutes1 = 0 if match1.group(5) == '' else int(match1.group(5))
            total = hours * 60 + minutes1
            minutes2 = int(match1.group(6))
            return {"name": field_name, "timing": float(total)}, {"name": match1.group(7), "timing": float(minutes2)}
        elif match2:
            minutes1 = int(match2.group(1)) * 60
            minutes2 = 15
            return {"name": field_name, "timing": float(minutes1)}, {"name": match2.group(2), "timing": float(minutes2)}

        return value


# приводим json к нужному виду
def transform_json():
    with open("corrected_data.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    transformed_data = []

    for entry in data:
        temp_data = {
            "temperature": entry["Температура"],
            "operations": []
        }

        for key, value in entry.items():
            if key != "Температура":
                transformed_value = transform_field(value, key)
                temp_data["operations"] += transformed_value

        transformed_data.append(temp_data)

    with open("corrected_data_2.json", 'w', encoding='utf-8') as file:
        json.dump(transformed_data, file, ensure_ascii=False, indent=4)


# избавляемся от пустых полей
def correct_json():
    with open('data.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)

    corrected_data = [{key: value for key, value in entry.items(
    ) if value is not None} for entry in data]
    with open('corrected_data.json', 'w', encoding='utf-8') as file:
        json.dump(corrected_data, file, ensure_ascii=False)


# создаем неформатированный json из таблицы и исправляем это
def run(data_frame: pd.DataFrame):
    selected_cols = data_frame.loc[:, 'Температура':].dropna(axis=1, how='all')
    selected_cols.to_json('data.json', orient='records', force_ascii=False)
    correct_json()
    transform_json()
    main.setup()
    for i in range(len(main.output_dataframe)):
        if not main.output_dataframe[i].empty:
            st.write(f"Печь - {i+1}")
            st.dataframe(main.output_dataframe[i])

            st.image(f'streamlit_app/back/image/{i}.png')


df = pd.DataFrame(
    columns=["Сплав", "Гр. спл.", "Кол. в садке, шт", "Бойки", "Температура",
             "Нагрев", "Подогрев", "Подогрев.1", "Подогрев.2", "Подогрев.3"],
)

agree = st.checkbox("Нажмите, если хотите загрузить excel-файл")
if agree:
    uploaded_table = st.file_uploader(
        "Выберите excel файл", type=['xls', 'xlsm', 'xlsx'])
    if uploaded_table is not None:
        df = pd.read_excel(uploaded_table)
        df = df.drop('статус', axis=1)
        df = correct_table(df)
        st.data_editor(df, num_rows="dynamic")

else:
    st.markdown(
        "**Формат для столбцов \"нагрев\" и \"подогрев\"**:  \n_N-N Nч+Nм ковка/прокат_ либо _Nч отжиг_.")
    st.write('Все в одну строчку.')
    st.data_editor(df, num_rows="dynamic")

button_clicked = st.button("Обработать", type='primary')
if button_clicked:
    run(df)
