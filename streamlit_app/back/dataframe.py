import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
sys.path.append("streamlit_app/back")

color_dict = {
    'otzhig': (1, 0.5, 0.08),
    'nagrev': 'y',
    'kovka': 'g',
    'prokat': (0.9, 0.4, 0.6)
}


def get_dataframe(ovens) -> pd.DataFrame:
    ouput = dict()
    for oven in ovens:
        data = {'operation': [], 'time_start': [],
                'time_end': [], 'durations': []}
        if len(ovens[oven]['time_list']) > 10:
            ovens[oven]['time_list'] = ovens[oven]['time_list'][:10]
        for oper in ovens[oven]['time_list']:

            data['operation'].append(oper[0])
            data['time_start'].append(oper[1])
            data['time_end'].append(oper[2])
            data['durations'].append(oper[2]-oper[1])

        # print(data)
        df = pd.DataFrame(data, columns=list(data.keys()))
        ouput[oven] = df
    return ouput


def make_diagramm(df, oven_inex):
    tasks = df['operation']
    start_dates = df['time_start']
    durations = df['durations']
    fig, ax = plt.subplots()

    # установим y лимит
    ax.set_yticks(np.arange(len(tasks)))
    ax.set_yticklabels(tasks)

    # рисуем все задачи
    for i in range(len(tasks)):
        start_date = start_dates[i]
        end_date = start_date + durations[i]
        color_for_task = color_dict[tasks[i]]
        ax.barh(i, end_date - start_date, left=start_date,
                height=0.5, align='center', color=color_for_task)

    # установим x-axis лимит
    min_date = min(start_dates)
    max_date = max(start_dates) + max(durations)
    ax.set_xlim(min_date, max_date)

    ax.set_xlabel('Date')
    ax.set_ylabel('Tasks')
    ax.set_title('Basic Gantt Chart')

    # сохраняем
    plt.grid(True)
    plt.savefig(f'streamlit_app/back/image/{oven_inex}.png')
