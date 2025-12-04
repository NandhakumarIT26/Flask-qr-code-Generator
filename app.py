from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_base64 = None
    error = None
    data = ''                # <- initialize here so it's always defined

    if request.method == 'POST':
        data = request.form.get('link', '').strip()
        if not data:
            error = 'Please enter a valid link.'
        else:
            # Create QR
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save to bytes buffer and convert to base64 for embedding in HTML
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode('ascii')
            qr_base64 = f"data:image/png;base64,{img_b64}"

    # Now it's safe to reference `data` (e.g. to preserve input back to the form)
    return render_template('index.html', qr=qr_base64, error=error, link_value=data)

if __name__ == '__main__':
    app.run(debug=True)
