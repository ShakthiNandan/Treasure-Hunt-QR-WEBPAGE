import qrcode
import json
import os
import uuid  # For unique codes
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Define paths
UPLOADS_DIR = "static/uploads"
QR_CODES_DIR = "static/qr_codes"
CODES_FILE = "static/codes.json"

# Ensure QR directory exists
os.makedirs(QR_CODES_DIR, exist_ok=True)

# Store unique codes
codes = {}

# Define colors for teams
team_colors = ["yellow", "red", "navy", "orange", "light blue", 
               "purple", "pink", "dark green", "light green", "brown"]


# Function to generate a stylized QR code
def generate_stylized_qr(text, filename, fg_color="black", bg_color="white", 
                         logo_path="logo.png", top_text="QR Code", number=1, invert_colors=False):
    qr = qrcode.QRCode(
        version=5,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=10,
        border=4,
    )
    
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill=fg_color, back_color=bg_color).convert("L").convert("RGBA")
    
    padding = 20
    qr_width, qr_height = qr_img.size
    new_width = qr_width + 2 * padding
    new_height = qr_height + 100  # Extra space for text
    
    final_img = Image.new("RGBA", (new_width, new_height), bg_color)
    final_img.paste(qr_img, (padding, 50))
    
    draw = ImageDraw.Draw(final_img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 25)
        num_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        num_font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), top_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    draw.text(((new_width - text_width) / 2, 10), top_text, font=font, fill=fg_color)

    num_text = str(number)
    num_bbox = draw.textbbox((0, 0), num_text, font=num_font)
    num_width = num_bbox[2] - num_bbox[0]
    num_height = num_bbox[3] - num_bbox[1]
    draw.text((new_width - num_width - 10, new_height - num_height - 10), num_text, font=num_font, fill=fg_color)

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
        x = (new_width - logo_size) // 2
        y = 50 + (qr_height - logo_size) // 2
        final_img.paste(logo, (x, y), logo)
    
    final_img.save(filename)
    print(f"Stylized QR Code saved as {filename}")
    
    if invert_colors:
        inverted_filename = filename.replace(".png", "_inverted.png")
        invert_qr_colors(filename, inverted_filename)

def invert_qr_colors(input_path, output_path):
    img = Image.open(input_path).convert("RGB")
    inverted_img = ImageOps.invert(img)
    inverted_img.save(output_path)
    print(f"Inverted QR saved as {output_path}")

# Get list of teams and assign colors
teams = sorted([team for team in os.listdir(UPLOADS_DIR) if os.path.isdir(os.path.join(UPLOADS_DIR, team))])
team_color_map = {team: team_colors[i % len(team_colors)] for i, team in enumerate(teams)}

# Generate QR codes for each audio file
for team_folder in teams:
    team_path = os.path.join(UPLOADS_DIR, team_folder)
    
    bg_color = team_color_map[team_folder]  # Assign color based on team

    for audio_file in os.listdir(team_path):
        if audio_file.endswith(".opus"):
            unique_code = str(uuid.uuid4())[:8]  # Generate random UUID
            codes[unique_code] = {
                "team": team_folder,
                "file": audio_file,
                "clue": audio_file.split(" ")[-1].split(".")[0]  # Extract clue number
            }

            n = audio_file.split(" ")[-1].split(".")[0] 
            url = f"http://TreasureHuntCIT.pythonanywhere.com/play/{unique_code}"
            qr_filename = os.path.join(QR_CODES_DIR, f"{unique_code}.png")
            generate_stylized_qr(url, qr_filename, bg_color=bg_color, top_text=f"{codes[unique_code]['team']}", number=n)
            
            print(f"Generated QR for {audio_file} -> {unique_code} with color {bg_color}")

# Save mappings to JSON
with open(CODES_FILE, "w") as f:
    json.dump(codes, f, indent=4)

print("All QR codes generated successfully!")
