<!-- Profile: meducae/meducae | Keep the assets folder beside this file. -->

<p align="center">
  <img src="./assets/dev-lab.gif" width="1200" alt="Soatmurod Xurramov — software engineer. Animated development workspace with x86-64 Assembly, hexadecimal characters and a conceptual neural network." />
</p>

<p align="center">
  <a href="https://github.com/meducae?tab=repositories"><img src="./assets/repositories.svg" height="36" alt="Explore my repositories" /></a>
  &nbsp;
  <a href="https://t.me/meducae"><img src="./assets/telegram.svg" height="36" alt="Connect on Telegram" /></a>
  &nbsp;
  <a href="https://www.linkedin.com/in/soatmurod-xurramov-7ba9b03a4/"><img src="./assets/linkedin.svg" height="36" alt="Connect on LinkedIn" /></a>
</p>

### `01 / whoami`

I'm **Soatmurod Xurramov**, a software engineer working across Android, cross-platform applications and backend systems. I care about clear architecture, efficient code and the details that make software reliable.

```yaml
current_focus:
  - AI integrations & machine learning
  - Kotlin Multiplatform
exploring:
  - Assembly & how software meets the machine
engineering:
  - SOLID principles & modular architecture
  - Response time & memory efficiency
```

### `02 / stack`

| Workspace | Technologies |
| :--- | :--- |
| **Mobile** | Kotlin · Dart · Flutter · Kotlin Multiplatform |
| **Backend** | Python · FastAPI · PHP |
| **Data & infrastructure** | MySQL · Docker · Linux · AWS |
| **Version control** | Git · GitHub |

### `03 / learning lab`

From CPU instructions to model inference — I like understanding what happens beneath the abstraction.

```python
# lab/model.py · a small neural layer, written explicitly
import numpy as np

def forward(x, weights, bias):
    z = x @ weights + bias
    return np.maximum(0, z)  # ReLU
```

<details>
<summary><strong>Open workspace.asm</strong> — the program in the banner</summary>

```asm
; Linux x86-64 · NASM syntax
section .data
    msg db "build. learn. repeat.", 10
    len equ $ - msg

section .text
global _start

_start:
    mov eax, 1
    mov edi, 1
    lea rsi, [rel msg]
    mov edx, len
    syscall

    mov eax, 60
    xor edi, edi
    syscall
```

The banner's signal flow and hexadecimal characters are a visual study of computation.

</details>

### `04 / engineering notes`

- **Architecture:** clear boundaries, focused modules and explicit dependencies.
- **Performance:** measure response time, memory use and the cost of abstractions.
- **Delivery:** build, test, observe and improve.

---

<p align="center">
  <samp>build. learn. repeat.</samp><br />
  <a href="https://t.me/meducae">Telegram</a> ·
  <a href="https://www.linkedin.com/in/soatmurod-xurramov-7ba9b03a4/">LinkedIn</a> ·
  <a href="https://github.com/meducae?tab=repositories">Explore the code</a>
</p>
