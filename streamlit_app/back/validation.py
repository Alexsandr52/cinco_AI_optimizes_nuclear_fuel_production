import model

# сделать печь недоступной на время и добавить эту информацию в кучу
def make_oven_busy(oven, global_time, busy_time=120) -> None:
    if oven['busy'] <= global_time:
        oven['busy'] = global_time+busy_time
    else:
        oven['busy'] += busy_time
    # busy_ovens.add(oven_id)

# # проверяем доступна ли печь если да то удаляем ее из списка не доступных
# def check_is_busy(oven_id) -> bool:
#     if ovens[oven_id]['busy'] <= global_time: return False
#     busy_ovens.remove(oven_id)
#     return True

# фиксируем врезя нача и конца обработки задачи печью и название задачи
def point_time(operation, oven, start_time ,busy_time=120) -> int:
    delay = start_time+busy_time
    oven['time_list'].append([operation, start_time, delay])
    return delay

def make_step(series, ovens, global_time):
    min_delay = 0
    
    for row in range(len(series)):
        series_one = series[row]
        # print(model)
        oven = ovens[model.predict(row)]
        total_delay = 0
        
        for oper in series_one['operations']:
            total_delay += oper['timing']

            # время начала работы печи для операции
            start_time = global_time if oven['busy'] <= global_time else oven['busy']
            # увеличевание переменной busy на время работы печи
            make_oven_busy(oven, global_time, oper['timing'])
            # запись времени начала и конца операции
            point_time(oper['name'], oven, start_time, oper['timing'])

        if min_delay == 0 or min_delay > total_delay: min_delay = total_delay

    return [min_delay, ovens]