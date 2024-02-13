from pprint import pp

from chart_ocr import chart_ocr


def full_test():
    errors = []
    for i in range(1301, 1501):
        try:
            i = f"0{i}" if i < 10 else str(i)
            print("test: ", i)
            pp(chart_ocr(f"data/{i}.png"))
        except Exception as e:  # noqa
            errors.append(i)
        finally:
            pp(f"{errors=}")
            print('---')
    print(f"{errors=}")


def single_test():
    result = chart_ocr(f"data/1489.png")
    pp(result)


if __name__ == '__main__':
    # full_test()
    single_test()

'''
errors (14):
1032 - цифра 7 наложилась на легенду
1105 - неверная сумма (1=4)
1172 - неверная сумма (23=28)
1189 - неверная сумма (8=79)
1197 - неверная сумма (8=79)
1202 - неверная сумма (8=79)
1219 - неверная сумма (8=79)
1233 - неверная сумма (1=4)
1314 - неверная сумма (8=79)
1344 - неверная сумма (8=79)
1395 - неверная сумма (8=79)
1420 - неверная сумма (8=79)
1444 - неверная сумма (10=40)
1489 - неверная сумма (8=79)
'''