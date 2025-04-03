from flask import Flask, render_template, send_from_directory, abort
import json
import os

app = Flask(__name__)

# Load unique codes
CODES_FILE = "static/codes.json"
with open(CODES_FILE, "r") as f:
    CODE_MAPPING = json.load(f)

@app.route("/")
def home():
    return "Welcome to Intellina 2K25 Treasure Hunt! Scan a QR code to get your clue."

@app.route("/play/<unique_code>")
def play_audio(unique_code):
    # Find file associated with the unique code
    if unique_code in CODE_MAPPING:
        team = CODE_MAPPING[unique_code]["team"]
        filename = CODE_MAPPING[unique_code]["file"]
        clue_number = CODE_MAPPING[unique_code]["clue"]

        return render_template(
            "player.html",
            team=team,
            filename=filename,
            clue_number=clue_number,
            unique_code=unique_code,
        )
    else:
        abort(404)

@app.route("/audio/<team>/<filename>")
def serve_audio(team, filename):
    directory = os.path.join("static", "uploads", team)
    return send_from_directory(directory, filename)

if __name__ == "__main__":
    app.run(debug=True)
