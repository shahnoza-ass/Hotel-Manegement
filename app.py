from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'yashirin_kalit'  # session ishlashi uchun

# ---- HOME va sahifalar ----
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/taomlar')
def taomlar():
    return render_template('taomlar.html')

@app.route('/ichimliklar')
def ichimliklar():
    return render_template('ichimliklar.html')

@app.route('/salatlar')
def salatlar():
    return render_template('salatlar.html')

@app.route('/shirinliklar')
def shirinliklar():
    return render_template('shirinliklar.html')

# ---- Savatchaga qo'shish ----
# @app.route('/add_to_cart', methods=['GET', 'POST'])
# def add_to_cart():
#     if request.method == 'POST':
#         item = request.form.get('item')
#     else:
#         item = request.args.get('item')
    
#     if item:
#         if 'cart' not in session:
#             session['cart'] = []
#         session['cart'].append(item)
#         session.modified = True
    
#     return redirect(request.referrer or url_for('home'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form.get('item')
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item)
    session.modified = True
    
    if 'redirect_to_cart' in request.form:  # Agar "Buyurtma berish" bosilsa
        return redirect(url_for('cart'))
    
    return redirect(request.referrer or url_for('home'))  # Aks holda oldingi sahifaga
#-------taomlar
@app.route('/nonushta')
def nonushta():
    return render_template('taomlar/nonushta.html')

@app.route('/tushlik')
def tushlik():
    return render_template('taomlar/tushlik.html')

@app.route('/kechki')
def kechki():
    return render_template('taomlar/kechki_ovqat.html')
#-------ichimliklar
@app.route('/salqin_ichimliklar')
def salqin_ichimliklar():
    return render_template('ichimliklar/salqin_ichimlik.html')

@app.route('/choylar')
def choylar():
    return render_template('ichimliklar/choylar.html')

@app.route('/qahva')
def qahva():
    return render_template('ichimliklar/kofe.html')

# ---- Savatcha oynasi ----
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart=cart_items)

@app.route('/jarayon')
def jarayon():
    return render_template('jarayon.html')

@app.route('/xonalar')
def xonalar():
    xonalar = list(range(101, 121))
    return render_template('xonalar.html', xonalar=xonalar)

@app.route('/restoran_xonalar')
def restoran_xonalar():
    xonalar = list(range(1, 45))
    return render_template('restorant_xonalar.html', xonalar=xonalar)
# Eski logikam
# @app.route('/clear_cart')
# def clear_cart():
#     session['cart'] = []
#     return redirect(url_for('home'))

@app.route('/remove_from_cart')
def remove_from_cart():
    item = request.args.get('item')
    if item and 'cart' in session:
        if item in session['cart']:
            session['cart'].remove(item)
            session.modified = True
    return redirect(url_for('cart'))  # Bu qatorni o'zgartiring


# Buyurtmalar uchun DB ni yaratish
def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Flask ishga tushganda DB ni ishga tushirish
init_db()
@app.route("/clear_cart")
def clear_cart():
    cart_items = session.get("cart", [])
    if cart_items:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO orders (items, date) VALUES (?, ?)", (
            ", ".join(cart_items),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
    session.pop("cart", None)
    return redirect(url_for('home'))

#### buyurtmalarni olish
@app.route('/buyurtmalarim')
def orders():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY date DESC")
    orders = c.fetchall()
    conn.close()
    return render_template("buyurtmalar.html", orders=orders)



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
