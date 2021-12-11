import json

class NotEnoughMoney(Exception):
    def __init__(self, msg):
        self.msg = msg
# with open('nominal.json', 'w') as file:
#     file.write(json.dumps(d))

# with open('nominal.json', 'r') as file:
#     reader = json.load(file)

reader = {"1000": 5, "500": 1, "200": 1, "100": 2, "50": 2, "20": 1, "10": 4}

def output_nominals(how_much, reader):
    nom = [int(i) for i in reader.keys() if reader[i] != 0] # [1000, 500, 200, 100, 50, 20]
    out = {'1000': 0, '500': 0, '200': 0, '100': 0, '50': 0, '20': 0, '10': 0}
    zapros = how_much
    flag = True
    while flag:
        flag = False
        if zapros // 1000 > 0 and reader['1000'] != 0 and \
                ((zapros - 1000) == 0 or [i for i in nom if ((zapros - 1000) // i) > 0]):
            reader['1000'] -= 1
            out['1000'] += 1
            zapros -= 1000
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 500 > 0 and reader['500'] != 0 and \
                ((zapros - 500) == 0 or [i for i in nom if ((zapros - 500) // i) > 0]):
            reader['500'] -= 1
            out['500'] += 1
            zapros -= 500
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 200 > 0 and reader['200'] != 0 and \
                ((zapros - 200) == 0 or [i for i in nom if ((zapros - 200) // i) > 0]):
            reader['200'] -= 1
            out['200'] += 1
            zapros -= 200
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 100 > 0 and reader['100'] != 0 and \
                ((zapros - 100) == 0 or [i for i in nom if ((zapros - 100) // i) > 0]):
            reader['100'] -= 1
            out['100'] += 1
            zapros -= 100
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 50 > 0 and reader['50'] != 0 and \
                ((zapros - 50) == 0 or [i for i in nom if ((zapros - 50) // i) > 0]):
            reader['50'] -= 1
            out['50'] += 1
            zapros -= 50
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 20 > 0 and reader['20'] != 0 and \
                ((zapros - 20) == 0 or [i for i in nom if ((zapros - 20) // i) > 0]):
            reader['20'] -= 1
            out['20'] += 1
            zapros -= 20
            if zapros == 0:
                break
            else:
                flag = True
        elif zapros // 10 > 0 and reader['10'] != 0 and \
                ((zapros - 10) == 0 or [i for i in nom if ((zapros - 10) // i) > 0]):
            reader['10'] -= 1
            out['10'] += 1
            zapros -= 10
            if zapros == 0:
                break
            else:
                flag = True

    result = []
    for k, v in out.items():
        result.append(int(k) * v)
    if sum(result) == how_much:
        return out
    else:
        raise NotEnoughMoney('БАНКОМАТ НЕ МОЖЕТ ВЫДАТЬ ДАННУЮ СУММУ!!!')

# print(output_nominals(1500, reader))
# print(output_nominals(1160, reader))
print(output_nominals(4280, reader))

