from PIL import Image
import os

def is_empty_frame(image):
    rgba_image = image.convert("RGBA")
    alpha = rgba_image.getchannel("A")
    return all(pixel == 0 for pixel in alpha.getdata())

image_path = "cat_sheet.png"
output_folder = "cat_gifs/"
image = Image.open(image_path)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
else:
    for f in os.listdir(output_folder):
        file_path = os.path.join(output_folder, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

rows = 10
cols = 8
width, height = image.size
piece_width = width // cols
piece_height = height // rows

for row in range(rows):
    frames = []

    for col in range(cols):
        left = col * piece_width
        upper = row * piece_height
        right = (col + 1) * piece_width
        lower = (row + 1) * piece_height

        piece = image.crop((left, upper, right, lower))

        if is_empty_frame(piece):
            continue

        piece_with_alpha = piece.convert("RGBA")
        frames.append(piece_with_alpha)

    if not frames:
        continue

    frames = [frame.convert("RGBA").convert("P", palette=Image.ADAPTIVE, dither=None) for frame in frames]

    row_gif_path = f"{output_folder}row_{row}.gif"
    frames[0].save(
        row_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,
        loop=0,
        transparency=0,
        disposal=2
    )

print(f"GIFs for rows saved in {output_folder}")
                        