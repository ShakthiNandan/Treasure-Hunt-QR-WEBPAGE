from PIL import Image
import os

def images_to_pdf(image_folder, output_pdf):
    images = []
    
    # Get all image files from the folder
    for file in sorted(os.listdir(image_folder)):
        if file.lower().endswith(('png', 'jpg', 'jpeg')):
            img_path = os.path.join(image_folder, file)
            img = Image.open(img_path).convert('RGB')
            images.append(img)
    
    if images:
        # Save the first image and append the rest
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF saved as {output_pdf}")
    else:
        print("No images found in the folder.")

# Example usage
image_folder = "static\\qr_codes\\"  # Change this to your folder path
output_pdf = "output.pdf"  # Output PDF file name
images_to_pdf(image_folder, output_pdf)
