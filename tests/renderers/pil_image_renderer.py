from flask import Flask, request
from src.naogi import NaogiModel, PilImageRenderer
from PIL import Image

app = Flask(__name__)

img = Image.open('tests/renderers/image.jpg')

def test_render_should_be_200():
  with app.test_request_context():
    resp = PilImageRenderer.render(img)
  assert resp.status_code == 200

def test_render_with_custom_format_should_be_200_and_imagejpeg_by_default():
  with app.test_request_context():
    resp = PilImageRenderer.render(img, 'JPEG')
  assert resp.status_code == 200
  assert resp.mimetype == 'image/jpeg'

def test_render_with_custom_format_should_be_200_and_with_correct_mime():
  with app.test_request_context():
    resp = PilImageRenderer.render(img, 'PNG', content_type='image/png')
  assert resp.status_code == 200
  assert resp.mimetype == 'image/png'

def test_model_render_with_custom_format_without_content_type():
  class TestModel(NaogiModel):
    def load_model(self):
      return super().load_model()
    def predict(self):
      return super().predict()
    def prepare(self):
      return super().prepare()
    def renderer(self):
      return PilImageRenderer
    def render_options_dict(self):
      return { 'content_format': 'PNG' }

  with app.test_request_context():
    model = TestModel()
    resp = model._render(img)
  assert resp.status_code == 200
  assert resp.mimetype == 'image/png'


def test_model_render_with_custom_format_with_content_type():
  class TestModel(NaogiModel):
    def load_model(self):
      return super().load_model()
    def predict(self):
      return super().predict()
    def prepare(self):
      return super().prepare()
    def renderer(self):
      return PilImageRenderer
    def render_options_dict(self):
      return { 'content_format': 'PNG', 'content_type': 'image/koko' }

  with app.test_request_context():
    model = TestModel()
    resp = model._render(img)
  assert resp.status_code == 200
  assert resp.mimetype == 'image/koko'
