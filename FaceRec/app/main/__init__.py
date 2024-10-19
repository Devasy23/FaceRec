from __future__ import annotations

from flask import Flask

from FaceRec.app.main.Edit import Edit_blueprint
from FaceRec.app.main.Employee import flk_blueprint
from FaceRec.app.main.Face import Face_Rec_blueprint
from FaceRec.app.main.VideoImage import employee_blueprint

app = Flask(
    __name__,
    template_folder="../../templates/",
    static_folder="../../static/",
)

# To register blueprints of Flask
try:
    app.register_blueprint(flk_blueprint)
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(Face_Rec_blueprint)
    app.register_blueprint(Edit_blueprint)
except Exception as e:
    print(f"Error registering blueprints: {e}")

# Function to run the server of Flask
def run_flask():
    try:
        app.run(host="127.0.0.1", port=5000)
    except Exception as e:
        print(f"Error running Flask server: {e}")
