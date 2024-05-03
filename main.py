from flask import Flask, request, jsonify
import psycopg2
import requests

app = Flask(__name__)

# Функция для обработки входящего вебхука
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        process_contact(data)
        return jsonify({'message': 'Webhook processed successfully'}), 200
    return jsonify({'message': 'Only POST requests are accepted'}), 405

# Функция для обработки контакта
def process_contact(data):
    # Получаем данные контакта
    contact_id = data['id']
    contact_name = data['name']

    # Подключение к БД PostgreSQL
    conn = psycopg2.connect(dbname='your_database', user='your_user', password='your_password', host='your_host')
    cur = conn.cursor()

    # Поиск имени в БД
    cur.execute("SELECT COUNT(*) FROM names_woman WHERE name = %s", (contact_name,))
    count_women = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM names_man WHERE name = %s", (contact_name,))
    count_men = cur.fetchone()[0]

    # Определение пола
    if count_women > 0:
        gender = 'Женщина'
    elif count_men > 0:
        gender = 'Мужчина'
    else:
        gender = 'Неопределен'

    # Обновление данных контакта в Битрикс24
    update_data = {'id': contact_id, 'gender': gender}
    response = requests.post('https://bitrix24-domain/rest/user.update', json=update_data)

    # Закрытие соединения с БД PostgreSQL
    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
