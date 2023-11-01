from flask import Flask, render_template, request
import os
import qrcode
from qrcode.image.svg import SvgImage

app = Flask(__name__)
UPLOAD_FOLDER = "static/qr_codes"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_qr(data, base_filename, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # For PNG
    png_filename = base_filename + '.png'
    img_png = qr.make_image(fill_color="black", back_color="white")
    img_png.save(png_filename)

    # For SVG
    svg_filename = base_filename + '.svg'
    img_svg = qr.make_image(image_factory=SvgImage, fill_color="black", back_color="white")
    img_svg.save(svg_filename)

    return png_filename, svg_filename

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        filename = request.form['filename']
        png_path, svg_path = generate_qr(data, os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # For download links
        png_link = png_path.replace("static", "/static")
        svg_link = svg_path.replace("static", "/static")

        return render_template('index.html', png_link=png_link, svg_link=svg_link)
    return render_template('index.html', png_link=None, svg_link=None)

if __name__ == "__main__":
    app.run(debug=True)

