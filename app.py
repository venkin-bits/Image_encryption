import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def xor_encrypt_decrypt(data: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in data])


def caesar_encrypt_decrypt(data: bytes, key: int) -> bytes:
    # Caesar shifts bytes by key modulo 256
    return bytes([(b + key) % 256 for b in data])


@app.route('/', methods=['GET', 'POST'])
def index():
    result_filename = None

    if request.method == 'POST':
        action = request.form.get('action')
        algorithm = request.form.get('algorithm')
        key = int(request.form.get('key'))
        file = request.files['image']
        filename = file.filename
        uploaded_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(uploaded_path)

        result_filename = f'{algorithm}_{action}_{filename}'
        result_path = os.path.join(RESULT_FOLDER, result_filename)

        with open(uploaded_path, 'rb') as f:
            data = f.read()

        if algorithm == 'xor':
            result_data = xor_encrypt_decrypt(data, key)
        elif algorithm == 'caesar':
            if action == 'decrypt':
                key = (-key) % 256
            result_data = caesar_encrypt_decrypt(data, key)
        else:
            result_data = data

        with open(result_path, 'wb') as f:
            f.write(result_data)

        return render_template('index.html', result_filename=result_filename)

    return render_template('index.html', result_filename=None)


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
