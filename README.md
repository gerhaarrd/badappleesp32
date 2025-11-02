# Bad Apple no ESP32 + OLED 128x64

🎬 Um projeto para rodar o famoso vídeo **Bad Apple** em OLED 0.96" (SSD1306/SH1106) usando **ESP32 e MicroPython**.  

O projeto inclui:
- Arquivo bin com os frames já convertidos para exibição no display.
- Script MicroPython para exibir o vídeo no display.

---

## 📦 Requisitos

- ESP32 (DevKitV1 ou similar)
- Display OLED 128x64 0.96" (SSD1306 ou SH1106)
- MicroPython instalado no ESP32
- Thonny IDE ou outra para enviar arquivos pro ESP32
- 2MB livre no ESP32
---

## 💾 Enviar para o ESP32

1. Conecte o ESP32 via USB e abra o **Thonny**.
2. No painel **Arquivos**, localize `frames.bin` no PC.
3. Clique com o botão direito → **“Enviar para /”** para copiar para o ESP32.

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
---

## 🔧 Dicas

* Se o arquivo `frames.bin` for muito grande, use SD card.

## 📼 Vídeos

<iframe width="560" height="315" src="https://www.youtube.com/embed/jC6i8l6ry9g?si=5Kiqm30ilyrkIFKY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## 📌 Licença

Projeto open source, sinta-se à vontade para adaptar e compartilhar.
Apenas dê crédito se usar este repositório como base.

---

✨ Divirta-se rodando Bad Apple no seu ESP32!



