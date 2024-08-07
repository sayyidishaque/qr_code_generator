import base64

from flask import Flask, render_template, request, send_file, url_for, redirect
import qrcode
from io import BytesIO

app = Flask(__name__)


def generate_qr_code(data, for_download=False):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    if for_download:
        return buffer

        # Encode the image to Base64 for displaying on the web page
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64


@app.route('/download', methods=['POST'])
def download():
    data = request.form.get('qr_code_data')
    if data:
        img = generate_qr_code(data, for_download=True)
        return send_file(img, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    img = None
    qr_code_data = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data:
            img = generate_qr_code(data)
            # return send_file(img, mimetype='image/png', as_attachment=True, download_name='qr_code.png')
    return render_template('index.html', img=img, qr_code_data=qr_code_data)


if __name__ == '__main__':
    app.run(debug=True)
