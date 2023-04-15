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
    return [[key, val[0], el['mark'], el['answer']] if not el['type'] == 'AO' else [key, val[0], el['mark'], el['choices'][el['answer']-1]] for (key, val), el in zip(dc.items(), q)]
