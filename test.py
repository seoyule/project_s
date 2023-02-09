#https://holypython.com/python-pil-tutorial/how-to-draw-shapes-on-images-python-ultimate-guide/
from PIL import Image, ImageDraw, ImageFilter, ImageFont

file_="/Users/seoyulejo/Downloads/imgs/1_SS 머매이드 스커트 (4color)/SS 머매이드 스커트 (4color)_1_rs.jpg"
img = Image.open(file_).convert("RGBA")
background = Image.new("RGBA", img.size, (0,0,0,0))

draw = ImageDraw.Draw(background)
draw.rounded_rectangle((397,447,530,483), 10, fill="WhiteSmoke", outline=None)
new_img = Image.composite(background, img, background)

# Typing inspirational quote and author's name on the new image with rounded rectangle/
draw2 = ImageDraw.Draw(new_img)

font2 = ImageFont.truetype("Arial.ttf", 30)
draw2.text((420,447), "Soyool", font=font2, fill='teal')




file_1 = "/Users/seoyulejo/Downloads/imgs/1_SS 머매이드 스커트 (4color)/SS 머매이드 스커트 (4color)_1_rs_1.jpg"
