from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Функция для подключения к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="Airport_DB",  # Название вашей базы данных
            user="postgres",  # Ваше имя пользователя
            password="1234509876",  # Ваш пароль
            host="localhost",  # Хост
            port="5432"  # Порт
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Просмотр доступных рейсов
@app.route('/flights')
def flights():
    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Flights WHERE status = 'Scheduled'")
        flights = cur.fetchall()
        conn.close()
        return render_template('flights.html', flights=flights)
    else:
        return "Ошибка подключения к базе данных."

# Регистрация пассажира
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        passport_number = request.form['passport_number']

        conn = connect_to_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO Passengers (first_name, last_name, passport_number)
                    VALUES (%s, %s, %s)
                    RETURNING passenger_id
                """, (first_name, last_name, passport_number))
                passenger_id = cur.fetchone()[0]
                conn.commit()
                conn.close()
                return redirect(url_for('buy_ticket', passenger_id=passenger_id))
            except Exception as e:
                conn.close()
                return f"Ошибка при регистрации пассажира: {e}"
        else:
            return "Ошибка подключения к базе данных."
    return render_template('register.html')

# Покупка билета
@app.route('/buy_ticket/<int:passenger_id>', methods=['GET', 'POST'])
def buy_ticket(passenger_id):
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        seat_number = request.form['seat_number']
        ticket_class = request.form['ticket_class']

        conn = connect_to_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO Tickets (flight_id, passenger_id, seat_number, class)
                    VALUES (%s, %s, %s, %s)
                """, (flight_id, passenger_id, seat_number, ticket_class))
                conn.commit()
                conn.close()
                return "Билет успешно куплен!"
            except Exception as e:
                conn.close()
                return f"Ошибка при покупке билета: {e}"
        else:
            return "Ошибка подключения к базе данных."

    conn = connect_to_db()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Flights WHERE status = 'Scheduled'")
        flights = cur.fetchall()
        conn.close()
        return render_template('buy_ticket.html', flights=flights, passenger_id=passenger_id)
    else:
        return "Ошибка подключения к базе данных."

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
