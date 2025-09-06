"""

_________________________________

 Author: https://vsc.rs

 pip install pillow

 Please copy arial.ttf font into working folder first!

 _________________________________

 """

from PIL import Image, ImageDraw, ImageFont

def measure_text(draw, text, font):
    try:
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        return right - left, bottom - top
    except Exception:
        return draw.textsize(text, font=font)

def draw_text_box(slika, tekst, x, y, w, h, font_path="arial.ttf",
                  max_font_size=100, min_font_size=10, fill=(0,0,0)):
    draw = ImageDraw.Draw(slika)

    # probaj od max ka min dok stane u okvir
    font_size = max_font_size
    while font_size >= min_font_size:
        font = ImageFont.truetype(font_path, font_size)
        tw, th = measure_text(draw, tekst, font)
        if tw <= w and th <= h:
            break
        font_size -= 1

    if font_size < min_font_size:  # fallback
        font = ImageFont.truetype(font_path, min_font_size)
        tw, th = measure_text(draw, tekst, font)

    # centriraj
    tx = x + (w - tw) // 2
    ty = y + (h - th) // 2

    draw.text((tx, ty), tekst, font=font, fill=fill)

def batch_slike(ulazna_slika, tekst_fajl, font_path="arial.ttf"):
    # Učitaj sve redove
    with open(tekst_fajl, "r", encoding="utf-8") as f:
        linije = [line.strip() for line in f if line.strip()]

    # Idi po parovima (tekst1, tekst2)
    for i in range(0, len(linije), 2):
        if i+1 >= len(linije):
            break  # ako nema drugog reda, preskoči

        tekst1 = linije[i]
        tekst2 = linije[i+1]

        # učitaj baznu sliku
        slika = Image.open(ulazna_slika).convert("RGB")

        # definiši pravougaonike za tekst
        # Please use mspaint or Incscape to find desired position and rect size of your text on Visit Card Picture Template (slika.jpg)
        
        rect1=(335, 1380, 1813, 97)    # x, y, w, h
        rect2=(1023, 1499, 465, 67)    # x, y, w, h        

        draw_text_box(slika, tekst1, *rect1, font_path=font_path,
                      max_font_size=120, min_font_size=12, fill=(0,0,0))
        draw_text_box(slika, tekst2, *rect2, font_path=font_path,
                      max_font_size=120, min_font_size=12, fill=(0,0,0))

        # ime izlazne slike (1, 2, 3…)
        broj = (i // 2) + 1
        izlaz = f"nova{broj}.jpg"
        slika.save(izlaz)
        print(f"[OK] Sačuvana {izlaz} sa tekstom: '{tekst1}' i '{tekst2}'")

# ------------------ Primer korišćenja ------------------
if __name__ == "__main__":
    batch_slike(
        ulazna_slika="slika.jpg",
        tekst_fajl="tekst.txt",
        font_path="arial.ttf"  # ili npr. "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )



"""

An important description first:

File tekst.txt contains names of your desired workers/students and comments bellow, for instance:

Mickey Joe
New York
Jhonny Cach
Kentucky
Hojima Kamura
Tokyo
...
etc.

"""
