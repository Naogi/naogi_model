from flask import Flask, request
from src.naogi import JsonRenderer
from PIL import Image
import json

app = Flask(__name__)

testing_dict = {'first': 1, 'second': 'Some text'}

def test_render_should_be_valid_json():
  with app.test_request_context():
    resp = JsonRenderer.render(testing_dict)
  assert resp == json.dumps(testing_dict)
