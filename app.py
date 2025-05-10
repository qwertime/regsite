from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'ЗАМЕНИТЕ_НА_СЛУЧАЙНУЮ_СТРОКУ'  # можно сгенерировать: import secrets; secrets.token_hex(16)

# —————— Настройки для Telegram-бота ——————
# 1) Создайте бота через @BotFather и получите BOT_TOKEN.
# 2) Запустите бота, напишите что-нибудь, откройте https://api.telegram.org/bot<7814079647:AAFqlLTEp3-8zuhsyB1RiEocI5Zb6WiiIMY/getUpdates
#    и найдите в ответе ваш chat_id – вставьте сюда:
BOT_TOKEN = '7814079647:AAFqlLTEp3-8zuhsyB1RiEocI5Zb6WiiIMY'
CHAT_ID   = '335343225'

def send_telegram_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print('Ошибка при отправке Telegram:', e)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd  = request.form['password']
        if user == '1111' and pwd == '2222':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Неверный логин или пароль')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/order_pass', methods=['POST'])
def order_pass():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['full_name']
    send_telegram_message(f'🆕 Запрос пропуска: {name}')
    flash('✅ Заявка отправлена администратору')
    return redirect(url_for('dashboard'))

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    rating = request.form['rating']
    # сохраняем в файл
    with open('ratings.txt', 'a', encoding='utf-8') as f:
        f.write(f'{rating}\n')
    flash(f'🙏 Спасибо за оценку: {rating}')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
