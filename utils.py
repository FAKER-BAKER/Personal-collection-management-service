def input_int(prompt: str, min_val: int = 0, max_val: int = 9999) -> int:
    while True:
        raw_val = input(prompt).strip()
        try:
            val = int(raw_val)
            if min_val <= val <= max_val:
                return val
            print(f"Число должно быть в диапазоне от {min_val} до {max_val}.")
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_float(prompt: str, min_val: float = 0.0) -> float:
    while True:
        raw_val = input(prompt).strip().replace(",", ".")
        try:
            val = float(raw_val)
            if val >= min_val:
                return val
            print(f"Значение не может быть меньше {min_val}.")
        except ValueError:
            print("Ошибка: введите корректное числовое значение.")


def input_non_empty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Поле не может быть пустым. Повторите ввод.")
