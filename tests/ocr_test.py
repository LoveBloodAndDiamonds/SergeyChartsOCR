from chart_ocr import chart_ocr


def check_result(chart_data: dict[str, list]):
    try:
        assert chart_data["Aug"] == ["35", "9", "20", "5"], "1"
        assert chart_data["Sep"] == ["31", "5", "15", "11"], "2"
        assert chart_data["Oct"] == ["31", "5", "15", "11"], "3"
        assert chart_data["Nov"] == ["31", "12", "18"], "4"
        print("Success")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    while True:
        result = chart_ocr(f"data/{input('num:')}.png")
        from pprint import pp
        pp(result)
        print()
    # check_result(result)
