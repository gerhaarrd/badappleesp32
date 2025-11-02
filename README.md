# Bad Apple no ESP32 + OLED 128x64

🎬 Um projeto para rodar o famoso vídeo **Bad Apple** em OLED 0.96" (SSD1306/SH1106) usando **ESP32 e MicroPython**.  

O projeto inclui:
- Conversão automática de PNGs monocromáticos para binário otimizado para SSD1306.
- Script MicroPython para exibir o vídeo no display.

---

## 📦 Requisitos

- ESP32 (DevKit ou similar)
- Display OLED 128x64 (SSD1306 ou SH1106)
- MicroPython instalado no ESP32
- Thonny IDE ou outra para enviar arquivos pro ESP32
- Python 3 no PC (para converter os PNGs)

---

## 🖼️ Preparar os frames

1. Coloque os **frames PNG monocromáticos** na pasta `frames_bin`.
2. Rode o script Python no PC (`converter.py`) para gerar `frames.bin`:

```python
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

            for page in range(HEIGHT // 8):
                for x in range(WIDTH):
                    byte = 0
                    for bit in range(8):
                        y = page * 8 + bit
                        if pixels[x, y] == 0:
                            byte |= (1 << bit)
                    f.write(bytes([byte]))
            print(f"✅ Convertido: {filename}")

print(f"\n🎬 Conversão finalizada! Arquivo salvo em: {output_file}")
````

* Cada frame terá 1024 bytes.
* O arquivo final `frames.bin` será usado no ESP32.

---

## 💾 Enviar para o ESP32

1. Conecte o ESP32 via USB e abra o **Thonny**.
2. No painel **Arquivos**, localize `frames.bin` no PC.
3. Clique com o botão direito → **“Enviar para /”** para copiar para o ESP32.

⚠️ Nota: ESP32 geralmente tem ~1–1.3 MB de espaço livre. Se o arquivo for maior, use SD card ou divida em partes.

---

## ⚡ Rodar o vídeo no ESP32

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

FRAME_SIZE = 1024
FPS = 15  # Ajuste conforme necessidade

with open('frames.bin', 'rb') as f:
    frame = f.read(FRAME_SIZE)
    while frame:
        oled.buffer = bytearray(frame)
        oled.show()
        frame = f.read(FRAME_SIZE)
```

* Para medir FPS real, rode a versão com **medidor de tempo**:

```python
start = time.ticks_ms()
frames = 0

with open('frames.bin', 'rb') as f:
    frame = f.read(FRAME_SIZE)
    while frame:
        oled.buffer = bytearray(frame)
        oled.show()
        frames += 1
        frame = f.read(FRAME_SIZE)

elapsed = time.ticks_diff(time.ticks_ms(), start)
fps = frames / (elapsed / 1000)
print("FPS médio:", fps)
```

---

## 🏎️ Otimizações

1. **Trocar para SPI** → muito mais rápido que I²C (até 3–4x).
2. **Biblioteca `.mpy` otimizada** → acelera atualização do display.
3. **Buffer fixo e `readinto()`** → reduz alocação de memória a cada frame.
4. **Pré-carregar frames na RAM** → se couber, elimina latência do sistema de arquivos.
5. **Calcular FPS real** → ajuste o tempo de `sleep()` para sincronização fluida.

---

## 🔊 Áudio e sincronização

* MicroPython + SSD1306 via I²C não permite 60 FPS com áudio simultâneo.
* Para sincronizar:

  1. Pré-calcular o tempo de cada frame.
  2. Tocar áudio via DAC/I²S em paralelo.
  3. Usar loop sincronizado com `time.ticks_ms()` em vez de `sleep()`.
* Alternativa avançada: usar **dois ESP32** (um só para áudio, outro só para vídeo).

---

## 🖌️ Telas maiores

* SSD1306 padrão: 0.96" (128×64)
* SH1106: 1.3" ou 1.54" (compatível com 128×64)
* SSD1309/1322: até 256×64, requer SPI + lib diferente
* Dica: dois SSD1306 lado a lado podem formar 256×64

---

## 🔧 Dicas finais

* Comece com FPS baixo (10–15) para testar.
* Use SPI + `.mpy` para velocidade máxima.
* Se o arquivo `frames.bin` for muito grande, use SD card.

---

## 📌 Licença

Projeto open source, sinta-se à vontade para adaptar e compartilhar.
Apenas dê crédito se usar este repositório como base.

---

✨ Divirta-se rodando Bad Apple no seu ESP32! 🎬🖤

```
```
