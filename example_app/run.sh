export FLASK_APP=example_app
export FLASK_DEBUG=true
export EXAMPLE_APP_CONFIG=config.cfg
pip install -e .
python -m flask run --host=0.0.0.0 --port=5000
