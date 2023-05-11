def solution_dict(dit: dict) -> dict:
    for key in dit: dit[key] = dit[key][0]
    return dit

def test_dict_to_list(lt: list):
    return [(el['answer'], el['text'], el['mark'], el['type'], el['choices']) if el['type'] == 'AO' else (el['answer'], el['text'], el['mark'], el['type']) for el in lt]

def generate_solution_file(test: list, solution: dict) -> dict:
    res = {}
    counter = [0, 0, 0]
    for q in test:
        match q[3]:
            case 'TF':
                counter[0] += 1
                ans = solution[f'TF_{counter[0]}']
                if ans == q[0]: res[q[1]] = [ans, q[2], q[2]]
                else: res[q[1]] = [ans, 0, q[2]]
            case 'O':
                counter[1] += 1
                ans = solution[f'O_{counter[1]}']
                if ans.lower() == q[0].lower(): res[q[1]] = [ans, q[2], q[2]]
                else: res[q[1]] = [ans, 0, q[2]]
            case 'AO':
                counter[2] += 1
                ans = solution[f'AO_{counter[2]}']
                if ans == '': res[q[1]] = ['Без ответа', 0, q[2]]
                elif int(ans) == q[0]: res[q[1]] = [q[4][int(ans)-1], q[2], q[2]]
                else: res[q[1]] = [q[4][int(ans)-1], 0, q[2]]
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