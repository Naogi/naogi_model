# naogi_model

NaogiModel it is an abstract class for the naogi.com ML deployment platform

## How to deploy via naogi.com
* Add `naogi` to your project requirements.txt
* create file `naogi.py` in the root directory (copypaste file from [naogi.py](https://github.com/Naogi/naogi_model))
* implement your logic of model loading, prepareing and calling
* go to you naogi.com profile, create project and connect git
<br>
<br>

## How it works? (What to implement in naogi.py)
### Loading model (server starting time)
When naogi server is starting, it call `load_model(self)` -- you have to implement model loading logic in that function (loading from file, internet, etc.)

Here you have to load and init your model and save the model object to some variable

Example
```python
def load_model(self):
  self.model = __get_model()
  self.model.load_weights()
```
<br>
<br>

### Prepareing (request time)
When you call [GET/POST] /prepare of your API `prepare(self, params_dict)` is calling first.

All request params can be found in `params_dict`. Here you can prepare you params: open and modify Image, transform and normalize text and safe data for `prepare` to self attribute.

Example
```python
# now you can make GET /predict?text_data=My-long-text
# (and not worry about spaces)
def prepare(self, params_dict):
  self.text = params_dict['text_data'].strip()
```
<br>
<br>

### Predicting (request time)
After request params prepareing `predict(self)` is calling.

```python
def predict(self):
  raw = self.model.predict(self.text)
  return __from_raw_to_some(raw)
```

Here you have to return the value, that valid for some Renderer class (json, file, custom)
<br>
<br>

### Rendering (request time)
And the last step is calling `renderer().render(...)` and passing the result of `predict`
Out of the box you can use `JsonRenderer` and `FileRenderer`

or

you can create custom renderer from `AbstractRenderer`
```python
class MyRenderer(AbstractRenderer):
  def render(data):
    return ...
```
```python
def renderer(self):
  return MyRenderer
```

`JsonRenderer` accepts any json.dumps valid data

`FileRenderer` uses flask's `send_file` under the hood, so you can pass any bytes. [Additional params can watch here](https://github.com/Naogi/naogi_model/blob/main/src/naogi/__init__.py#L17)

<br>
<br>

### Fin
And finally you can make API calls to `<your-naogi-project-url>/predict` with params


## Development
...

### Testing
Before testing you should install **pytest**

From root folder
```shell
PYTHONPATH='./' pytest tests/renderers/pil_image_renderer.py
```

### Deploy
```shell
rm -rf dist/*
python3 -m build
python3 -m twine upload --repository pypi dist/*
```
