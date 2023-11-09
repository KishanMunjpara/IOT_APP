import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS
import qrcode
from io import BytesIO
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
conn = mysql.connector.connect(host="sql12.freemysqlhosting.net", user="sql12660589", password="LHH6JzN9pj",
                               database="sql12660589")
cursor = conn.cursor()

CORS(app)


@app.route('/')
def choose_way():
    return render_template('Choose_Way.html')


@app.route('/login')
def login():
    return render_template('Parent_login.html')


@app.route('/register')
def about():
    return render_template('Parent_register.html')


@app.route('/home')
def home():
    if 'id' in session:
        user_id = session['id']
        cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id}")
        user_data = cursor.fetchone()
        if user_data:
            user_profile = {
                'name': user_data[1],
                'rollno': user_data[2],
                'class': user_data[3],
                'email': user_data[4],
                'password': user_data[5],
                'mobile': user_data[6]
            }
            return render_template('Parent_home.html', user_profile=user_profile)
        else:
            return "User data not found."
    else:
        return redirect('/login')


@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    data = request.get_json()
    value = data['data']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'qrcode': 'data:image/png;base64,' + img_str})


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    rollno = request.form.get('urollno')
    Class = request.form.get('uclass')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    mobile = request.form.get('umobile')

    cursor.execute(
        """INSERT INTO  `users`(`id`,`name`,`rollno`,`class`,`email`,`password`,`mobile`) VALUES (NULL,'{}','{}','{}','{}','{}','{}')""".format(
            name, rollno, Class, email, password, mobile))
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['id'] = myuser[0][0]
    return redirect('/home')


@app.route('/logout')
def logout():
    if 'id' in session:
        session.pop('id')
    return redirect('/login')


# School Login
@app.route('/School_login')
def school_login():
    return render_template('School_login.html')


@app.route('/School_register')
def school_register():
    return render_template('School_Register.html')


@app.route('/School_home')
def school_home():
    if 'id' in session:
        user_id = session['id']
        cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id}")

        user_data = cursor.fetchone()
        if user_data:
            user_profile = {
                'name': user_data[1],
                'rollno': user_data[2],
                'class': user_data[3],
                'email': user_data[4],
                'password': user_data[5],
                'mobile': user_data[6]
            }
            return render_template('School_home.html', user_profile=user_profile)
        else:
            return "User data not found."
    else:
        return redirect('/School_login')


@app.route('/School_generate_qr_code', methods=['POST'])
def school_generate_qr_code():
    data = request.get_json()
    value = data['data']

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(value)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return jsonify({'qrcode': 'data:image/png;base64,' + img_str})


@app.route('/School_login_validation', methods=['POST'])
def school_login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['id'] = users[0][0]
        return redirect('/School_home')
    else:
        return redirect('/School_login')


@app.route('/School_add_user', methods=['POST'])
def school_add_user():
    name = request.form.get('uname')
    rollno = request.form.get('urollno')
    Class = request.form.get('uclass')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    mobile = request.form.get('umobile')

    cursor.execute(
        """INSERT INTO  `users`(`id`,`name`,`rollno`,`class`,`email`,`password`,`mobile`) VALUES (NULL,'{}','{}','{}','{}','{}','{}')""".format(
            name, rollno, Class, email, password, mobile))
    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['id'] = myuser[0][0]
    return redirect('/School_home')


@app.route('/School_logout')
def school_logout():
    if 'id' in session:
        session.pop('id')
    return redirect('/School_login')


@app.route('/scanner')
def qrcode_scanner():
    # Get the video capture device
    cap = cv2.VideoCapture(0)

    # Create a barcode scanner object
    barcode_decoder = cv2.QRCodeDetector()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Decode barcodes in the frame
        decoded_info, points, _ = barcode_decoder.detectAndDecode(frame)

        # If a barcode is detected, print the information
        if points is not None:
            if isinstance(points, list):
                points = np.array(points, dtype=np.int32)

            if points.shape == (4, 1, 2):
                cv2.polylines(frame, [points], True, (255, 0, 0), 5)

            if decoded_info:
                print("Decoded information: ", decoded_info)
                break

        # Display the resulting frame
        cv2.imshow('Barcode reader', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    app.run(debug=True)
