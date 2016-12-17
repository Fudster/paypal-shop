import flask
from paypalrestsdk.notifications import WebhookEvent
from dbconnect import connection
from MySQLdb import escape_string as thwart
from decimal import Decimal
import pal
app = flask.Flask(__name__, static_url_path='')
c, conn = connection()

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'GMRKMGKRMG',
)
def app_start(host,port):
    app.run(host=host, port=port)   

@app.route('/order', methods=['GET', 'POST'])
def order():
    email = flask.request.form['email']
    pid = flask.request.form['pid']
    quantity = flask.request.form['quantity']
    username = flask.request.form['username']
    print(email + pid + quantity + username)
    start_order(email,pid,quantity,username)
    return "OK"

    
@app.route('/hook', methods=['GET', 'POST'])
def hook():
    event_body = flask.request.get_json()
    event_body2 = str(event_body)
    transmission_id = flask.request.headers['Paypal-Transmission-Id']
    timestamp = flask.request.headers['Paypal-Transmission-Time']
    actual_signature = flask.request.headers['Paypal-Transmission-Sig']
    cert_url = flask.request.headers['Paypal-Cert-Url']
    auth_algo = flask.request.headers['PayPal-Auth-Algo']
    print(event_body["event_type"])
    
    response = WebhookEvent.verify(
        transmission_id, timestamp, "9H062197GW227400A", event_body2, cert_url, actual_signature, auth_algo)
    print(response)
  
    return ('', 200)

def get_price(x,quantity):
    c.execute("SELECT price FROM product WHERE sid=%s", [x])
    data = float(c.fetchone()[0])
    price = data / 1000
    return price * quantity
def get_name(x):
    c.execute("SELECT name FROM product WHERE sid=%s", [x])
    data = str(c.fetchone()[0])
    return data

def insert_data(email,pid,quantity,username,invoice,price):
    c.execute("INSERT INTO `order`(`invoice`, `product`, `username`, `quantity`, `email`, `status`) VALUES (%s, %s, %s, %s, %s, %s);",
                          (thwart(invoice), thwart(pid), thwart(username), thwart(quantity), thwart(email), thwart("NP") ))
    c.execute("SELECT LAST_INSERT_ID();")
    order = str(c.fetchone()[0])
    c.execute("INSERT INTO `invoice`(`invoice`, `price`, `order`, `status`) VALUES (%s, %s, %s, %s);",
                          (thwart(invoice), price, thwart(order), "NP"))
    
def start_order(email,pid,quantity,username):
    price = get_price(pid,int(quantity))
    name = get_name(pid)
    invoice = (pal.create(email,name,price))
    insert_data(email,pid,quantity,username,invoice,price)
    
    
app_start('0.0.0.0',6060)