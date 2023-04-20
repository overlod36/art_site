def solution_dict_to_list(dit: dict):
    return [(dit[key][0], key) for key in dit]

def test_dict_to_list(lt: list):
    return [(el['answer'], el['text'], el['mark'], el['choices']) if el['type'] == 'AO' else (el['answer'], el['text'], el['mark']) for el in lt]

def generate_solution_file(test: list, solution: list):
    res = {}
    for i in range(len(solution)):
        match solution[i][1][0]:
            case 'T':
                if solution[i][0] == test[i][0]: res[test[i][1]] = [solution[i][0], test[i][2], test[i][2]]
                else: res[test[i][1]] = [solution[i][0], 0, test[i][2]]
            case 'O':
                if solution[i][0].lower() == test[i][0].lower(): res[test[i][1]] = [solution[i][0], test[i][2], test[i][2]]
                else: res[test[i][1]] = [solution[i][0], 0, test[i][2]]
            case 'A':
                if int(solution[i][0]) == test[i][0]: res[test[i][1]] = [test[i][3][int(solution[i][0]) - 1], test[i][2], test[i][2]]
                else: res[test[i][1]] = [test[i][3][int(solution[i][0]) - 1], 0, test[i][2]]
    return res

def get_test_attempt_list(dc: dict, q: list):
    return [[key, val[0], el['mark'], el['answer'], val[1]] if not el['type'] == 'AO' else [key, val[0], el['mark'], el['choices'][el['answer']-1], val[1]] for (key, val), el in zip(dc.items(), q)]

def set_test_attempt(attempt: dict, points: list):
    i = 0
    for key in attempt:
        attempt[key][1] = points[i]
        i += 1
    return attempt

def get_test_points(dc: dict):
    return sum([el['mark'] for el in dc['questions']])

def get_test_attempt_points(dc: dict):
    return sum(dc[el][1] for el in dc)