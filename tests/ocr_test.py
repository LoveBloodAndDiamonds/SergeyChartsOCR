from pprint import pp

from chart_ocr import chart_ocr


def full_test():
    errors = []
    for i in range(1, 51):
        try:
            i = f"0{i}" if i < 10 else str(i)

            print(i)
            result = chart_ocr(f"data/{i}.png")

            from pprint import pp
            pp(result)
            print()
        except Exception as e:
            errors.append(i)
        finally:
            print(errors)
            print('---')
    print(f"{errors=}")


def single_test():
    result = chart_ocr(f"data/70.png")
    pp(result)


if __name__ == '__main__':
    single_test()
