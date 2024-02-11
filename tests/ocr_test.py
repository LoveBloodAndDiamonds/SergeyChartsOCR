from chart_ocr import chart_ocr
from pprint import pp


if __name__ == '__main__':
    # while True:
    # ['17', '20', '29', '31', '32', '33', '36', '37', '40']
    # errors = []
    # for i in range(1, 51):
    #     try:
    #         i = f"0{i}" if i < 10 else str(i)
    #
    #         print(i)
    #         result = chart_ocr(f"data/{i}.png")
    #
    #         from pprint import pp
    #         pp(result)
    #         print()
    #     except Exception as e:
    #         errors.append(i)
    #     print(errors)
    #     print('---')
    # a = ['17_252', '20_177', '29_252', '31_97', '32_105', '33_190',
    #      '36_212', '37_235', '40_101']
    # result = chart_ocr(f"data/40.png")
    # pp(result)

    # ['32', '33', '37']
    result = chart_ocr(f"data/11.png")
    print(result)
