from PIL import Image
import os

input_folder = "frames_bin"
output_file = "frames.bin"

WIDTH = 128
HEIGHT = 64

with open(output_file, "wb") as f:
    for filename in sorted(os.listdir(input_folder)):
        if filename.lower().endswith(".png"):
            path = os.path.join(input_folder, filename)
            img = Image.open(path).convert("1")
            img = img.resize((WIDTH, HEIGHT))
            pixels = img.load()

            # percorre por páginas (8 linhas verticais por vez)
            for page in range(HEIGHT // 8):
                for x in range(WIDTH):
                    byte = 0
                    for bit in range(8):
                        y = page * 8 + bit
                        if pixels[x, y] == 0:  # pixel preto = aceso
                            byte |= (1 << bit)
                    f.write(bytes([byte]))
            print(f"✅ Convertido: {filename}")

print(f"\nconversão finalizada. arquivo salvo em: {output_file}")
