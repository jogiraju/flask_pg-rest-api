from app import create_app, db, User

app = create_app()

#Entry point for Flask CLI (flask run) allows using flask shell with direct access to db and User (handy for debugging)
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User}
