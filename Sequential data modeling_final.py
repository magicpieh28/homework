import numpy as np


b1, b2, b3 = 1.0, 2.0, 3.0

very = 'very'
Not = 'not'
good = 'good'
bad = 'bad'

x1, x2 = 'x1', 'x2'

table = {very :1.0, Not :0.0, good : 1.0, bad : 0.0}
no1 = {x1 : table[very], x2 : table[good]}
no2 = {x1 : table[Not], x2 : table[good]}
no3 = {x1 : table[Not], x2 : table[bad]}
no4 = {x1 : table[very], x2 : table[bad]}
no = [no1, no2, no3, no4]

lr = 0.1


class Model():
    def __init__(self, num):
        self.num = num

    def forward(num: dict):
        X1 = [num[x1] * w for w in weight1[:3]] #[x1w11, x1w12, x1w13]
        X2 = [num[x2] * w for w in weight1[3:]] #[x2w14, x2w15, x2w16]

        X = [x1 + x2 for (x1, x2) in zip(X1, X2)] #[(X1[0] + X2[0]), (X1[1] + X2[1]), (X1[2] + X2[2])]
        AF1 = [np.tanh(x) for x in X] #[tanh(X[0]), tanh(X[1]), tanh(X[2])]
        AF2 = [x * w for (x, w) in zip(AF1, weight2)] #[AF1[0]w21, AF1[1]w22, AF1[2]w23]
        output = np.tanh(np.sum(AF2)) #tanh(sum(AF2))
        print(f'output => {output}')
        return output


    def loss(num: dict):
        f = Model.forward(num)
        if num is no1 or num is no3:
            print(f'loss => {np.square(1 - f) / 2}')
            return np.square(1 - f) / 2
        else:
            print(f'loss => {np.square(-1 - f) / 2}')
            return np.square(-1 - f) / 2


    def backward(num: dict):
        X1 = [num[x1] * w for w in weight1[:3]] #[x1w11, x1w12, x1w13]
        X2 = [num[x2] * w for w in weight1[3:]] #[x2w14, x2w15, x2w16]
        X = [x1 + x2 for (x1, x2) in zip(X1, X2)] #[(X1[0] + X2[0]), (X1[1] + X2[1]), (X1[2] + X2[2])]

        one = 1 - np.square(np.tanh(Model.forward(num)))

        two = []
        for idx, w in enumerate(weight1):
            if idx is 0 or idx is 3:
                two.append((1 - np.square(np.tanh(X[0]))) * weight2[0])
            elif idx is 1 or idx is 4:
                two.append((1 - np.square(np.tanh(X[1]))) * weight2[1])
            else:
                two.append((1 - np.square(np.tanh(X[2]))) * weight2[2])
        two = [one * item for item in two]

        three = []
        for (item, w) in zip(two, weight1):
            if w not in weight1[:3]:
                three.append(item * num[x2])
            else:
                three.append(item * num[x1])

        result_1 = [w + lr * item for (item, w) in zip(three, weight1)]
        result_2 = [one * np.tanh(X[i]) for i, w in enumerate(weight2)]
        if num is no1 or num is no3:
            result_1 = [-(1 - Model.forward(num)) * item for item in result_1]
            result_2 = [-(1 - Model.forward(num)) * item for item in result_2]
        else:
            result_1 = [-(-1 - Model.forward(num)) * item for item in result_1]
            result_2 = [-(-1 - Model.forward(num)) * item for item in result_2]

        print(f'result_1 => {result_1}')
        print(f'result_2 => {result_2}')
        return result_1, result_2


w11, w12, w13, w14, w15, w16 = (b2+1), -(b3+1), (b1+1), (b1+1), \
                               (b2+1), -(b3+1)
w21, w22, w23 = -(b1+1), -(b2+1), -(b3+1)
weight1, weight2 = [w11, w12, w13, w14, w15, w16], [w21, w22, w23]
weight1 = [w / 10 for w in weight1]
weight2 = [w / 10 for w in weight2]
print(weight1, weight2)


for idx, n in enumerate(no):
    print(f'\n\n{idx+1}')
    Model.forward(n)
    Model.loss(n)
    weight1, weight2 = Model.backward(n)
