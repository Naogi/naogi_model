from flask import Flask, request
from src.naogi import  PilImageRenderer
from PIL import Image

app = Flask(__name__)

img = Image.open('tests/renderers/image.jpg')

def test_render_should_be_200():
  with app.test_request_context():
    resp = PilImageRenderer.render(img)
  assert resp.status_code == 200

def test_render_with_custom_format_should_be_200():
  with app.test_request_context():
    resp = PilImageRenderer.render(img, 'PNG')
  assert resp.status_code == 200
