#https://holypython.com/python-pil-tutorial/how-to-draw-shapes-on-images-python-ultimate-guide/
from PIL import Image, ImageDraw, ImageFilter, ImageFont

file_="/Users/seoyulejo/Downloads/imgs/1_속기모 베이직조거 셋트가능 빅사이즈 남녀공용/속기모 베이직조거 셋트가능 빅사이즈 남녀공용_1.jpg"
img = Image.open(file_)
#.convert("RGBA")
cropped = img.crop((623,971,879,1035))
blurred = cropped.filter(ImageFilter.GaussianBlur(radius=10))
img.paste(blurred,(623,971,879,1035))

draw = ImageDraw.Draw(background)
draw.rectangle((623,971,879,1035), fill= 255)

new_img = Image.composite(background, img, background)

# Typing inspirational quote and author's name on the new image with rounded rectangle/
draw2 = ImageDraw.Draw(new_img)

font2 = ImageFont.truetype("Arial.ttf", 30)
draw2.text((420,447), "Soyool", font=font2, fill='teal')




file_1 = "/Users/seoyulejo/Downloads/imgs/1_SS 머매이드 스커트 (4color)/SS 머매이드 스커트 (4color)_1_rs_1.jpg"
