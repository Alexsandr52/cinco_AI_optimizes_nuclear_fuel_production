import dataframe
import validation
import model
import json
import sys
sys.path.append("streamlit_app/back")

global_time = 0
end_time = 1440

output_dataframe = None

iteration = 100
# печи
ovens = {}
# серии
series = {}

# все операции которые можно выполнить
operations = set()
# все возможные температуры
temps_set = set()

# пути к данным печей и серий
oven_json_path = 'streamlit_app/back/oven.json'
series_json_path = 'corrected_data_2.json'


def init():
    # читаем печи
    with open(oven_json_path, 'rb') as f:
        data = json.load(f)
        for i, oven in enumerate(data['ovens']):
            oven['busy'] = 0
            oven['time_list'] = list()
            operations.update(oven['operations'])
            temps_set.update(oven['working_temps'])
            ovens[i] = oven

    trans = {
        'нагрев': 'nagrev',
        'ковка': 'kovka',
        'подогрев': 'nagrev',
        'подогрев.1': 'nagrev',
        'подогрев.2': 'nagrev',
        'подогрев.3': 'nagrev',
        'отжиг': 'otzhig',
        'прокат': 'prokat'

    }
    # читаем серии
    with open(series_json_path, 'rb') as f:
        data = json.load(f)
        for i, ser in enumerate(data):
            ser['operations'] = [
                {'name': trans[el['name']], 'timing': el['timing']} for el in ser['operations']]
            series[i] = ser

    # создаем матрицу и обучаем
    model.create_marix(len(series), len(ovens))
    for i in range(iteration):
        model.fit_model(series, ovens)


def setup():
    init()
    weights = model.weights
    global ovens
    global global_time
    global output_dataframe

    for i in range(3):
        min_delay, ovens = validation.make_step(series, ovens, global_time)
        global_time += min_delay

    output_dataframe = dataframe.get_dataframe(ovens)
    print(output_dataframe)
    for df_id in output_dataframe:
        if output_dataframe[df_id].empty:
            continue
        dataframe.make_diagramm(output_dataframe[df_id], df_id)
