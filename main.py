import tkinter as tk
from tkinter import messagebox
import string


# Функція для відкриття файлу та обробки даних
def open_file(version):
    file_path = entry_file.get()  # Отримуємо шлях до файлу з поля введення
    if not file_path:
        messagebox.showerror("Помилка", "Введіть назву файлу!")  # Перевірка на пусте поле
        return

    try:
        # Відкриваємо файл для читання
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()  # Зчитуємо вміст файлу
            result = process_data(data, version)  # Обробляємо дані
            text_result.delete(1.0, tk.END)  # Очищуємо текстове поле
            text_result.insert(tk.END, result)  # Виводимо результат
    except FileNotFoundError:
        messagebox.showerror("Помилка", "Файл не знайдено!")  # Повідомлення про відсутність файлу
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося прочитати файл: {str(e)}")  # Інші помилки


# Функція для обробки тексту
def process_data(data, version):
    # Видаляємо знаки пунктуації з тексту
    translator = str.maketrans('', '', string.punctuation)
    cleaned_data = data.translate(translator)

    # Розділяємо текст на слова
    words = cleaned_data.split()

    # Видаляємо однобуквені слова
    words = [word for word in words if len(word) > 1]

    # Фільтруємо слова, де друга буква "е" (у нижньому регістрі)
    filtered_words = [word for word in words if len(word) > 1 and word[1].lower() == 'е']

    # Якщо обрано варіант "а", обмежуємо довжину слів до 10 символів
    if version == 'a':
        filtered_words = [word for word in filtered_words if len(word) <= 10]

    # Якщо відфільтровані слова відсутні, повертаємо повідомлення
    if not filtered_words:
        return "Слів з другою буквою 'e' не знайдено."

    # Знаходимо найдовше слово
    longest_word = max(filtered_words, key=len)

    # Якщо є кілька слів з однаковою довжиною, вибираємо останнє
    longest_words = [word for word in filtered_words if len(word) == len(longest_word)]
    longest_word = longest_words[-1]

    # Повертаємо результат
    return f"Найдовше слово з другою буквою 'e': {longest_word}"


# Функція для збереження результату у файл
def save_result():
    result = text_result.get(1.0, tk.END).strip()  # Отримуємо результат з текстового поля
    if not result:
        messagebox.showerror("Помилка", "Немає результату для збереження!")  # Перевірка на пустий результат
        return

    try:
        # Зберігаємо результат у файл
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        messagebox.showinfo("Успіх", "Результат збережено у файл 'result.txt'!")  # Повідомлення про успіх
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти результат: {str(e)}")  # Повідомлення про помилку


# Функція для відображення інформації про програму
def show_about():
    about_text = (
        "Програма для обробки текстових файлів\n"
        "Автор: Самойленко Алла\n"
        "Група: 124-23з-1\n\n"
        "Опис: Програма дозволяє знайти найдовше слово з другою буквою 'e'. \n"
        "Є два варіанти виконання програми: \n"
        "з обмеженням на кількість символів в слові та без обмежень."
    )
    messagebox.showinfo("Про програму", about_text)  # Вікно з інформацією


# Функція для отримання опису завдання
def get_task_description():
    return "ЗАВДАННЯ 4.\n\nЗнайти найдовше слово серед слів, друга буква яких 'e'."


# Функція для відкриття вікна завдання
def open_task(version):
    global entry_file, text_result
    task_window = tk.Toplevel(root)  # Створюємо нове вікно
    task_window.title(f"Завдання 4 ({'a' if version == 'a' else 'b'})")
    task_window.geometry("900x700")

    # Відображаємо опис завдання
    label_task = tk.Label(task_window, text=get_task_description(), font=("Arial", 12))
    label_task.pack(pady=10)

    frame = tk.Frame(task_window)
    frame.pack(padx=10, pady=10)

    # Поле для введення шляху до файлу
    label_file = tk.Label(frame, text="Назва файлу:")
    label_file.grid(row=0, column=0, sticky='w')

    entry_file = tk.Entry(frame, width=50)
    entry_file.grid(row=0, column=1, padx=5, pady=5)

    # Кнопка для відкриття файлу
    button_open = tk.Button(frame, text="Відкрити файл", command=lambda: open_file(version))
    button_open.grid(row=0, column=2, padx=5, pady=5)

    # Текстове поле для виведення результату
    text_result = tk.Text(frame, width=80, height=15)
    text_result.grid(row=1, column=0, columnspan=3, pady=10)

    # Кнопка для збереження результату
    button_save = tk.Button(frame, text="Зберегти результат", command=save_result)
    button_save.grid(row=2, column=1, pady=10)


# Головне вікно програми
root = tk.Tk()
root.title("Головне меню")
root.geometry("600x500")

# Назва завдання
label_task_main = tk.Label(root, text="Виберіть завдання:", font=("Arial", 12))
label_task_main.pack(pady=10)

# Кнопка для запуску завдання 4, варіант "а" (з обмеженням символів)
button_task_a = tk.Button(
    root,
    text="Запустити завдання 4, \nВаріант а \nз обмеженням символів до 10 символів в слові",
    command=lambda: open_task('a')
)
button_task_a.pack(pady=5)

# Кнопка для запуску завдання 4, варіант "б" (без обмежень)
button_task_b = tk.Button(
    root,
    text="Запустити завдання 4, \nВаріант б \nбез обмежень символів в слові.",
    command=lambda: open_task('b')
)
button_task_b.pack(pady=5)

# Кнопка для відображення інформації про програму
button_about = tk.Button(root, text="Про програму", command=show_about)
button_about.pack(pady=5)

# Запуск головного циклу програми
root.mainloop()