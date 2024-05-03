import psycopg2
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Подключение к PostgreSQL базе данных
conn = psycopg2.connect(
    database="your_database",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)

# Создание таблицы для задач, если её нет
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_text TEXT
        )
    """)
    conn.commit()

# Функция для добавления задачи в базу данных
def add_task(update: Update, context: CallbackContext):
    task_text = ' '.join(context.args)
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (task_text) VALUES (%s)", (task_text,))
        conn.commit()
    update.message.reply_text('Задача добавлена!')

# Функция для вывода списка задач
def list_tasks(update: Update, context: CallbackContext):
    with conn.cursor() as cursor:
        cursor.execute("SELECT task_text FROM tasks")
        tasks = cursor.fetchall()
    if tasks:
        task_list = "\n".join([f"{index + 1}. {task[0]}" for index, task in enumerate(tasks)])
        update.message.reply_text(f"Список задач:\n{task_list}")
    else:
        update.message.reply_text("Список задач пуст")

def main():
    updater = Updater("TOKEN", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("add", add_task))
    dp.add_handler(CommandHandler("tsk", list_tasks))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
