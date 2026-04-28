import math
from typing import List, Tuple


class HillCipher:
    def __init__(self, m: int = 26):
        self.m = m

    def multiply(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])

        if cols_A != rows_B:
            raise ValueError("Нельзя перемножить матрицы")

        result = [[0] * cols_B for _ in range(rows_A)]

        for i in range(rows_A):
            for j in range(cols_B):
                s = 0
                for k in range(cols_A):
                    s += A[i][k] * B[k][j]
                result[i][j] = s % self.m

        return result

    def determinant(self, matrix: List[List[int]]) -> int:
        """Вычисление определителя матрицы (2x2 и 3x3)"""
        n = len(matrix)

        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        elif n == 3:
            a, b, c = matrix[0]
            d, e, f = matrix[1]
            g, h, i = matrix[2]
            return (a * e * i + b * f * g + c * d * h -
                    c * e * g - b * d * i - a * f * h)
        else:
            raise ValueError("Поддерживаются только матрицы 2x2 и 3x3")

    def mod_inverse(self, a: int) -> int:
        """Обратный элемент по модулю m (расширенный алгоритм Евклида)"""
        a = a % self.m
        for x in range(1, self.m):
            if (a * x) % self.m == 1:
                return x
        raise ValueError(f"{a} не имеет обратного по модулю {self.m}")

    def cofactor(self, matrix: List[List[int]], row: int, col: int) -> int:
        minor = []
        for i in range(len(matrix)):
            if i == row:
                continue
            minor_row = []
            for j in range(len(matrix)):
                if j == col:
                    continue
                minor_row.append(matrix[i][j])
            minor.append(minor_row)

        det_minor = self.determinant(minor)

        return det_minor * ((-1) ** (row + col))

    def inverse_matrix(self, matrix: List[List[int]]) -> List[List[int]]:
        """Обратная матрица по модулю m (для 2x2 и 3x3)"""
        n = len(matrix)

        if n == 2:
            a, b = matrix[0]
            c, d = matrix[1]

            det = (a * d - b * c) % self.m

            if math.gcd(det, self.m) != 1:
                raise ValueError(f"Определитель {det} не обратим")

            det_inv = self.mod_inverse(det)

            inv = [
                [(d * det_inv) % self.m, ((-b) * det_inv) % self.m],
                [((-c) * det_inv) % self.m, (a * det_inv) % self.m]
            ]
            return inv

        elif n == 3:
            det = self.determinant(matrix) % self.m

            if math.gcd(det, self.m) != 1:
                raise ValueError(f"Определитель {det} не обратим")

            det_inv = self.mod_inverse(det)

            # Вычисляем миноры
            cofactor_matrix = [[0] * 3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    cofactor_matrix[i][j] = self.cofactor(matrix, i, j)

            # Транспонируем присоединенную матрицу
            adjugate = [[0] * 3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    adjugate[i][j] = cofactor_matrix[j][i] % self.m

            # Умножаем на det^(-1)
            inv = [[0] * 3 for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    inv[i][j] = (adjugate[i][j] * det_inv) % self.m

            return inv

        else:
            raise ValueError("Поддерживаются только матрицы 2x2 и 3x3")

    def text_to_numbers(self, text: str) -> List[int]:
        return [ord(ch.upper()) - ord('A') for ch in text if ch.isalpha()]

    def numbers_to_text(self, nums: List[int]) -> str:
        return ''.join(chr((n % self.m) + ord('A')) for n in nums)

    def encrypt(self, text: str, key: List[List[int]]) -> str:
        nums = self.text_to_numbers(text)
        n = len(key)

        # Дополняем текст
        while len(nums) % n != 0:
            nums.append(23)  # 'X'

        result = []

        for i in range(0, len(nums), n):
            block = [[x] for x in nums[i:i + n]]
            encrypted = self.multiply(key, block)
            result.extend([row[0] for row in encrypted])

        return self.numbers_to_text(result)

    def decrypt(self, ciphertext: str, key: List[List[int]]) -> str:
        inv_key = self.inverse_matrix(key)
        return self.encrypt(ciphertext, inv_key)

    def Hill_demo(self):
        print("ШИФР ХИЛЛА")

        key2x2 = [
            [3, 3],
            [2, 5]
        ]

        print(f"Пример 1: \nКлюч 2x2:")
        for row in key2x2:
            print(f"  {row}")

        text = "HELLO"
        print(f"\nИсходный текст: {text}")

        ciphertext = self.encrypt(text, key2x2)
        print(f"Зашифрованный текст: {ciphertext}")

        decrypted = self.decrypt(ciphertext, key2x2)
        print(f"Расшифрованный текст: {decrypted}")

        inv2x2 = self.inverse_matrix(key2x2)
        print(f"\nОбратная матрица 2x2:")
        for row in inv2x2:
            print(f"  {row}")

        key3x3 = [
            [1, 2, 3],
            [0, 1, 4],
            [5, 6, 0]
        ]

        print(f"\n\nПример 2: \nКлюч 3x3:")
        for row in key3x3:
            print(f"  {row}")

        det3x3 = self.determinant(key3x3)
        det_mod = det3x3 % 26

        if math.gcd(det_mod, 26) == 1:
            plaintext3 = "PYTHON"
            print(f"\nИсходный текст: {plaintext3}")

            ciphertext3 = self.encrypt(plaintext3, key3x3)
            print(f"Зашифрованный текст: {ciphertext3}")

            decrypted3 = self.decrypt(ciphertext3, key3x3)
            print(f"Расшифрованный текст: {decrypted3}")

            inv3x3 = self.inverse_matrix(key3x3)
            print(f"\nОбратная матрица 3x3:")
            for row in inv3x3:
                print(f"  {row}")

            product3x3 = self.multiply(key3x3, inv3x3)

            is_identity = all(product3x3[i][j] == (1 if i == j else 0) for i in range(3) for j in range(3))
            print(f"\nПроверка: {'Обратная матрица составлена верно' if is_identity else 'Ошибка!'}")
        else:
            print(f"Определитель {det_mod} НЕ обратим по модулю 26")
            print("Нужно выбрать другую матрицу\n")

    def cryptoanalize_demo(self):
        print("ВЗЛОМ ШИФРА ХИЛЛА 2×2 ПО ИЗВЕСТНОМУ ТЕКСТУ")

        secret_key = [[7, 8], [11, 11]]

        known_text = "HELLO"
        known_ciphertext = self.encrypt(known_text, secret_key)

        print(f"Открытый текст: {known_text}")
        print(f"Шифротекст: {known_ciphertext}")

        nums_p = self.text_to_numbers(known_text)
        nums_c = self.text_to_numbers(known_ciphertext)

        P = [[nums_p[0], nums_p[2]], [nums_p[1], nums_p[3]]]
        C = [[nums_c[0], nums_c[2]], [nums_c[1], nums_c[3]]]

        detP = self.determinant(P) % 26
        print(f"\nP = {P}")
        print(f"det(P) mod 26 = {detP} (обратим: {math.gcd(detP, 26) == 1})")
        print(f"C = {C}")

        P_inv = self.inverse_matrix(P)
        recovered_key = self.multiply(C, P_inv)

        print(f"\nP**-1 = {P_inv}")
        print(f"Восстановленный ключ K = C × P**-1 = {recovered_key}")
        print(f"Ключ верен: {recovered_key == secret_key}")

        new_ciphertext = self.encrypt("ATTACKATDAWN", secret_key)
        decrypted = self.decrypt(new_ciphertext, recovered_key)

        print(f"\nНовый перехваченный шифротекст: {new_ciphertext}")
        print(f"Расшифровано украденным ключом:   {decrypted}")


class RecurrentHillCipher:
    def __init__(self, m: int = 26):
        self.m = m
        self.hill = HillCipher(m)

    def rec_encrypt(self, text: str, K1: List[List[int]], K2: List[List[int]]) -> str:
        nums = self.hill.text_to_numbers(text)
        n = len(K1)

        while len(nums) % n != 0:
            nums.append(23)  # 'X'

        keys = [K1, K2]
        blocks_count = len(nums) // n
        while len(keys) < blocks_count:
            keys.append(self.hill.multiply(keys[-2], keys[-1]))

        result = []
        for i in range(0, len(nums), n):
            block = [[x] for x in nums[i:i + n]]
            encrypted = self.hill.multiply(keys[i // n], block)
            result.extend(row[0] for row in encrypted)

        return self.hill.numbers_to_text(result)

    def rec_decrypt(self, ciphertext: str, K1: List[List[int]], K2: List[List[int]]) -> str:
        nums = self.hill.text_to_numbers(ciphertext)
        n = len(K1)

        keys = [K1, K2]
        inv_keys = [self.hill.inverse_matrix(K1), self.hill.inverse_matrix(K2)]
        blocks_count = len(nums) // n

        while len(inv_keys) < blocks_count:
            keys.append(self.hill.multiply(keys[-2], keys[-1]))
            inv_keys.append(self.hill.inverse_matrix(keys[-1]))

        result = []
        for i in range(0, len(nums), n):
            block = [[x] for x in nums[i:i + n]]
            decrypted = self.hill.multiply(inv_keys[i // n], block)
            result.extend(row[0] for row in decrypted)

        return self.hill.numbers_to_text(result)

    def rec_Hill_demo(self):
        print("\nРЕКУРРЕНТНЫЙ ШИФР ХИЛЛА")

        K1_3x3 = [
            [1, 2, 3],
            [0, 1, 4],
            [5, 6, 0]
        ]

        K2_3x3 = [
            [2, 5, 3],
            [1, 3, 2],
            [3, 1, 5]
        ]

        print(f"K1 (3x3):")
        for row in K1_3x3:
            print(f"  {row}")

        print(f"\nK2 (3x3):")
        for row in K2_3x3:
            print(f"  {row}")

        det1 = self.hill.determinant(K1_3x3) % 26
        det2 = self.hill.determinant(K2_3x3) % 26

        print(f"\nОпределитель K1 mod 26: {det1} (обратим: {math.gcd(det1, 26) == 1})")
        print(f"Определитель K2 mod 26: {det2} (обратим: {math.gcd(det2, 26) == 1})")

        if math.gcd(det1, 26) == 1 and math.gcd(det2, 26) == 1:
            longtext = "LONGTEXTFORENCRYPTION"
            print(f"\nИсходный текст: {longtext}")

            longciphertext = self.rec_encrypt(longtext, K1_3x3, K2_3x3)
            print(f"Зашифрованный текст: {longciphertext}")

            longdecrypted = self.rec_decrypt(longciphertext, K1_3x3, K2_3x3)
            print(f"Расшифрованный текст: {longdecrypted}")

            if longdecrypted == longtext.upper():
                print("\nШифрование и дешифрование работают корректно!\n")
            else:
                print("\nОшибка при шифровании/дешифровании\n")
        else:
            print("Матрицы не обратимы!")


if __name__ == "__main__":
    hill = HillCipher(26)
    recurrent = RecurrentHillCipher(26)

    hill.Hill_demo()
    recurrent.rec_Hill_demo()
    hill.cryptoanalize_demo()




