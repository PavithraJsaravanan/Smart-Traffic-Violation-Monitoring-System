from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import qrcode
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class Violation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20))
    violation_type = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date = db.Column(db.String(20))
    fine_amount = db.Column(db.Integer)
    status = db.Column(db.String(10), default="Unpaid")
@app.route('/')
def index():
    violations = Violation.query.all()
    return render_template('index.html', violations=violations)
@app.route('/add', methods=['GET','POST'])
def add_violation():
    if request.method == 'POST':
        v = Violation(
            vehicle_number=request.form['vehicle'],
            violation_type=request.form['type'],
            location=request.form['location'],
            date=request.form['date'],
            fine_amount=request.form['fine']
        )
        db.session.add(v)
        db.session.commit()
        return redirect('/')
    return render_template('add_violation.html')
@app.route('/pay/<int:id>')
def pay(id):
    violation = Violation.query.get(id)
    violation.status = "Paid"
    db.session.commit()
    return redirect('/')
@app.route('/qr/<int:id>')
def generate_qr(id):
    import os
    if not os.path.exists("static"):
        os.makedirs("static")
    url = f"http://127.0.0.1:5000/status/{id}"
    img = qrcode.make(url)
    path = f"static/qr_{id}.png"
    img.save(path)
    return f"<h3>QR Code Generated</h3><img src='/{path}'>"
@app.route('/status/<int:id>')
def status(id):
    violation = Violation.query.get(id)
    return render_template('status.html', violation=violation)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)