from PIL import Image, ImageOps
import os

def add_frame(input_folder, output_folder, frame_image_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        frame_image = Image.open(frame_image_path)
    except IOError:
        print(f"Error: Unable to open frame image at {frame_image_path}")
        return

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            try:
                image = Image.open(img_path)
            except IOError:
                print(f"Error: Unable to open image {img_path}")
                continue

            # Resize frame to match the size of the image
            frame_resized = frame_image.resize(image.size, Image.LANCZOS)

            # Make sure the frame is in RGBA mode
            if frame_resized.mode != 'RGBA':
                frame_resized = frame_resized.convert('RGBA')

            # Make sure the image is in RGBA mode
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # Composite the frame on top of the image
            framed_image = Image.alpha_composite(image, frame_resized)

            # Save the result
            output_path = os.path.join(output_folder, filename)
            framed_image.save(output_path, 'PNG')

            print(f"Frame added to {filename}")

if __name__ == "__main__":
    input_folder = input("Enter the path to the input folder: ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()
    frame_image_path = input("Enter the path to the frame image: ").strip()

    add_frame(input_folder, output_folder, frame_image_path)
