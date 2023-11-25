import numpy as np

# Матрица весов для модели
weights = None


def create_marix(n, m):
    global weights 
    weights = np.full((n, m), 10)

def fit_model(series, ovens):
    for row in range(len(weights)):
        series_one = series[row]
        col_chooise = 0
        prize = 0
        penalty = 0

        max_element = weights[row][0]
        for col in range(len(weights[row])):
            if weights[row][col] > max_element:
                max_element = weights[row][col]
                col_chooise = col

        if ovens[col_chooise]['start_temp']!= series_one['temperature']: penalty -= 1
        else: prize += 0.5

        for i in range(len(series_one['operations'])):
            if series_one['operations'][i]['name'] in ovens[col_chooise]['operations']: prize += 0.5
            else: penalty -= 1
        
        if series_one['temperature'] in ovens[col_chooise]['working_temps']: prize += 1.5
        else: penalty -= 2
        
        weights[row][col_chooise] += penalty + prize
        
def predict(row):
    oven = 0
    max_element = weights[row][0]
    for col in range(len(weights[row])):
        if weights[row][col] > max_element:
            max_element = weights[row][col]
            oven = col
    return oven

