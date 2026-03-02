from PIL import Image, ImageDraw, ImageFont
import os


def add_watermark_to_directory(directory, text, output_dir=None, font_path=None, font_size=20):
    """Apply a semi-transparent text watermark to all JPG/PNG images in a directory."""
    if output_dir is None:
        output_dir = directory
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        input_path = os.path.join(directory, filename)
        img = Image.open(input_path).convert("RGBA")

        # make watermark layer
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)
        # choose font
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
        textwidth, textheight = draw.textsize(text, font)
        # position bottom right
        x = img.width - textwidth - 10
        y = img.height - textheight - 10
        draw.text((x, y), text, font=font, fill=(255,255,255,128))

        watermarked = Image.alpha_composite(img, txt)
        output_path = os.path.join(output_dir, filename)
        watermarked.convert('RGB').save(output_path)


if __name__ == '__main__':
    # example usage
    add_watermark_to_directory('app/static/img/productos', 'almapunt.es')
