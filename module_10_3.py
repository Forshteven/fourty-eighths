import random, time, threading
from threading import Lock


class Bank:
    def __init__(self):
        # Начальный баланс банка
        self.balance = 0

        # Блокировка для синхронизации доступа к балансу
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            # Генерируем случайную сумму для пополнения
            amount = random.randint(50, 500)

            with self.lock:
                # Увеличиваем баланс
                self.balance += amount

                print(f"Пополнение: {amount}. Баланс: {self.balance}")

                if self.balance >= 500:
                    # Если баланс больше или равен 500, разблокируем замок
                    self.lock.release()

            # Задержка для имитации времени обработки
            time.sleep(0.001)

    def take(self):
        for i in range(100):
            # Генерируем случайную сумму для снятия
            amount = random.randint(50, 500)

            with self.lock:
                print(f"Запрос на {amount}")

                if amount <= self.balance:
                    # Если сумма доступна, уменьшаем баланс
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    # Если суммы недостаточно, блокируем замок
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()


if __name__ == "__main__":
    bk = Bank()

    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    print(f"Итоговый баланс: {bk.balance}")