from chart_ocr import chart_ocr
from pprint import pp


if __name__ == '__main__':
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
    #     finally:
    #         print(errors)
    #         print('---')

    result = chart_ocr(f"data/49.png")
    print(result)
