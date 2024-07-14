export FLASK_APP=run.py
export FLASK_ENV=development

uvicorn src:app --reload