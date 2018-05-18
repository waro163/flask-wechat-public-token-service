import os
from app import create_app,db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # app_context = app.app_context()
    # app_context.push()
    # db.create_all()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)