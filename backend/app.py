import sqlalchemy as sa
import sqlalchemy.orm as so
from flaskr import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'sa': sa, 'so': so}