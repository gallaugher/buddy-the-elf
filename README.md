# Buddy the Elf

A cardboard cutout of Buddy the Elf that waves, talks, and pops open a candy box. Trigger him by touching the bows on his gift, or from your phone over Bluetooth with Adafruit's free Bluefruit Connect app.

Built on an [Adafruit Circuit Playground Bluefruit](https://www.adafruit.com/product/4333) running CircuitPython.

**Build video, with the complete parts list and step-by-step instructions:**
[MakerSnack – Buddy the Elf](https://youtu.be/AHcwQRxTjOY)

By Prof. John Gallaugher — [gallaugher.com](https://gallaugher.com) · [@gallaugher](https://bsky.app/profile/gallaugher.bsky.social) · [YouTube.com/profgallaugher](https://youtube.com/profgallaugher)

---

## What's in this repo

| File / folder | What it is |
|---|---|
| `code.py` | The CircuitPython program. Copy it to the root of the `CIRCUITPY` drive. |
| `sounds/` | Eleven short Buddy quotes as `.wav` files. Copy the whole folder to `CIRCUITPY`. |
| `README.md` | This file. |

The sound clips are included as a non-commercial learning example. They are short excerpts from a copyrighted film, so please treat them accordingly and swap in your own audio if you share or remix this project.

---

## What it does

- **Touch a bow** on the wrapped gift and Buddy raises his arm, waves while a clip plays, then lowers it again.
- **Touch the fifth bow** and the candy box lid pops open, then eases closed over about six seconds.
- **Connect the Bluefruit Connect app** and the Control Pad's eight buttons trigger specific quotes, a random quote, or the candy box.
- Touch keeps working the whole time, whether or not a phone is connected.

---

## Parts

The video has the full list with links. The electronics are:

| Part | Notes |
|---|---|
| [Circuit Playground Bluefruit](https://www.adafruit.com/product/4333) | nRF52840 board with Bluetooth LE, capacitive touch pads, onboard speaker amp |
| [Adafruit STEMMA Speaker – Plug and Play Audio Amplifier](https://www.adafruit.com/product/3885) | Enclosed speaker with a built-in class-D amp. Takes 3–5 V power and a 0–3 V audio signal on a 3-pin JST PH connector. |
| [JST PH 3-pin Plug to Color-Coded Alligator Clips cable](https://www.adafruit.com/product/4030) | Plugs into the STEMMA speaker; the three clips (white, red, black) grab the CPB's pads |
| Two standard 180° hobby servos | One waves Buddy's arm, one lifts the candy box lid |
| Alligator clip test leads | For the servo wires and the touch bows |
| Thin copper wire | Runs from each bow, under the wrapping paper, out to an alligator clip |
| Micro-USB cable and a USB wall adapter or power bank | Buddy runs on USB power |

Plus a printed Buddy cutout, cardboard, a box to wrap as the gift, bows, and a small box with a hinged lid for the candy.

---

## Wiring

Everything attaches to the pads around the edge of the Circuit Playground Bluefruit with alligator clips, so there's no soldering.

### Speaker

The STEMMA speaker plugs into the JST-to-alligator-clip cable, and the three clips go to the CPB:

| Cable wire | STEMMA speaker pin | CPB pad |
|---|---|---|
| White | Signal | **A0 / AUDIO** (the pad next to the onboard speaker) |
| Red | Power (3–5 V) | **VOUT** |
| Black | Ground | **GND** |

`A0 / AUDIO` carries the same PWM audio that feeds the onboard speaker, so the little onboard speaker plays too. If you want *only* the external speaker, change `speaker.value = True` to `False` near the top of `code.py`.

VOUT passes through whatever is powering the board (5 V from USB), which gives the amp the most headroom. The 3.3 V pad also works if you want it quieter.

### Servos

Servos have three wires: signal (orange or yellow), power (red), and ground (brown or black).

| Servo | Signal wire → CPB pad | Power → | Ground → |
|---|---|---|---|
| Wave servo (Buddy's arm) | **A1** | VOUT | GND |
| Lid servo (candy box) | **TX** | VOUT | GND |

Power the servos from **VOUT**, not 3.3 V. Servos draw brief bursts of current when they start moving, and the 3.3 V regulator can't keep up; VOUT is fed straight from USB.

### Touch bows

The five bows on the gift are capacitive touch sensors. A length of copper wire runs from under each bow, beneath the wrapping paper, and out to an alligator clip on one of the CPB's touch pads:

| Bow | CPB pad | What it does |
|---|---|---|
| Bow 1 | **A2** | Plays *"My name's Buddy"* |
| Bow 2 | **A3** | Plays *"Christmas cheer… sing loud"* |
| Bow 3 | **A4** | Plays *"Santa's coming, so much to do"* |
| Bow 4 | **A5** | Plays a random quote from the rest of the list |
| Bow 5 | **A6** | Pops open the candy box |

`A1` and `TX` would normally be touch pads too, but they're busy driving the servos, which is why the bows start at `A2`.

### Pad map at a glance

```
A0 / AUDIO  →  speaker signal (white clip)
VOUT        →  speaker power (red clip) + both servo power leads
GND         →  speaker ground (black clip) + both servo ground leads
A1          →  wave servo signal
TX          →  lid servo signal
A2 – A6     →  touch bows 1–5
```

---

## Sound files

All clips live in `/sounds/` on the `CIRCUITPY` drive. `code.py` keeps them in a list, and the index in that list is what the touch pads and app buttons refer to:

| # | File | Triggered by |
|---|---|---|
| 0 | `my-names-buddy.wav` | Bow 1 · App button 1 |
| 1 | `christmas-cheer-sing-loud.wav` | Bow 2 · App button 2 |
| 2 | `santas-coming-so-much-to-do.wav` | Bow 3 · App button 3 |
| 3 | `its-great-to-meet-you.wav` | Random (Bow 4 or App button 4) |
| 4 | `i-just-like-to-smile.wav` | App ← · Random |
| 5 | `you-sit-on-a-throne-of-lies.wav` | App ↓ · Random |
| 6 | `you-did-it.wav` | Random |
| 7 | `whats-a-christmas-gram.wav` | Random |
| 8 | `i-love-you.wav` | Random |
| 9 | `santa-i-know-him.wav` | Random |
| 10 | `santa-must-have-called-you.wav` | Random |

Bow 4 picks randomly from clips 3–10 (so it never repeats the three clips that have their own bows). App button 4 picks randomly from all eleven.

**Adding your own clips:** CircuitPython wants **16-bit PCM, mono WAV** files. **22,050 Hz** is the safe sample rate; the Bluefruit will also play 44,100 Hz mono files, and a few of the clips here are. Audacity (File → Export → WAV, "Signed 16-bit PCM", set the project rate to 22050 and Tracks → Mix → Mix Stereo Down to Mono) or `ffmpeg -i in.mp3 -ac 1 -ar 22050 -sample_fmt s16 out.wav` will do it. Drop the file in `sounds/` and add its name to the `buddySounds` list in `code.py`.

---

## Using the Bluefruit Connect app

1. Install **Bluefruit Connect** — free on the [App Store](https://apps.apple.com/app/adafruit-bluefruit-le-connect/id830125974) and [Google Play](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect).
2. Power up Buddy. The board advertises itself as **"Buddy the Elf"** (set by `ble.name` in `code.py`).
3. Open the app, find **Buddy the Elf** in the device list, and tap **Connect**.
4. Choose **Controller**, then **Control Pad**.

The Control Pad has four numbered buttons and four arrows:

| Button | Buddy does… |
|---|---|
| **1** | *"My name's Buddy"* |
| **2** | *"Christmas cheer… sing loud"* |
| **3** | *"Santa's coming, so much to do"* |
| **4** | A random quote (any of the eleven) |
| **▲ Up** | Pops open the candy box |
| **▼ Down** | *"You sit on a throne of lies"* |
| **◄ Left** | *"I just like to smile"* |
| **► Right** | Makes the touch bows less sensitive (see Troubleshooting) |

Buddy waves whenever a clip plays, no matter how it was triggered.

If the app still shows the board's old `CIRCUITPYxxxx` name, your phone has cached it. Toggle Bluetooth off and on and scan again.

---

## How the code works

**Setup.** `code.py` turns on the speaker amp, creates five `touchio.TouchIn` objects for pads A2–A6, and sets up two servos through `pwmio.PWMOut` at 50 Hz and the `adafruit_motor.servo` library. The lid servo starts at 115° (lid closed) and the wave servo at 0° (arm down). The `BLERadio` is named "Buddy the Elf" and given a Nordic UART service, which is what Bluefruit Connect talks to.

**Playing a clip.** `playfile()` opens the WAV, hands it to `audiopwmio.PWMAudioOut` on the `SPEAKER` pin, and starts it playing. While the audio is going it runs the wave choreography: `moveUp()` raises the arm from 0° to 50°, `move()` swings it between 50° and 135° and back, over and over, until `audio.playing` goes false, then `moveBack()` lowers it to rest. Everything is wrapped in `with` blocks so the file and the audio hardware are released after every clip.

**Opening the box.** `openLid()` snaps the servo to 0° (the lid flies open) and then steps it back to 115° one degree every 50 ms, so the lid closes gently over about six seconds.

**Touch.** `checkTouch()` loops through the five pads. Pads 0–2 play the clip with the same index; pad 3 plays a random clip from index 3 onward; pad 4 opens the lid.

**The main loop.** The board starts advertising over Bluetooth and calls `checkTouch()` continuously while it waits for a phone. Once connected, it keeps polling touch and also checks `uart_server.in_waiting`. Only when the app has sent bytes does it call `Packet.from_stream()`; without that check `from_stream()` would block waiting for data on every pass and the bows would feel laggy. A `ButtonPacket` with `pressed == True` is matched against the Control Pad buttons in the table above. When the phone disconnects, the outer loop starts advertising again.

**Why `with` and `in_waiting` matter.** Every clip re-creates the `PWMAudioOut`, so releasing it cleanly after each play keeps the PWM hardware free for the servos. And because the program never sleeps in the main loop, touch response stays snappy in both the connected and unconnected states.

---

## Installing

1. Install the current release of **CircuitPython** (9.x or later) on the Circuit Playground Bluefruit: [circuitpython.org/board/circuitplayground_bluefruit](https://circuitpython.org/board/circuitplayground_bluefruit/).
2. Download the **Adafruit CircuitPython Library Bundle** that matches your CircuitPython major version: [circuitpython.org/libraries](https://circuitpython.org/libraries). Copy these folders into `CIRCUITPY/lib/`:
   - `adafruit_ble`
   - `adafruit_bluefruit_connect`
   - `adafruit_motor`
3. Copy `code.py` to the root of `CIRCUITPY`.
4. Copy the `sounds` folder to the root of `CIRCUITPY`, so the files are at `CIRCUITPY/sounds/*.wav`.
5. The board restarts automatically and starts advertising. Touch a bow or connect with the app.

The serial console (Mu, Thonny, or `screen`) prints which pad was touched and which clip is playing, which is handy while you're getting the bows dialed in.

---

## Troubleshooting

**A bow triggers on its own, or won't trigger.** Capacitive touch thresholds are calibrated when the board powers up, so power it on with the bows in their final position and nobody touching them. If a bow is too twitchy, press **► Right** in the Control Pad — each press raises every pad's threshold by 50 and prints the before/after values to the serial console. To make it permanent, set `touchpad[i].threshold` right after the pads are created in `code.py`.

**`ImportError` or `Incompatible .mpy file`.** The `.mpy` library format changed in CircuitPython 9 and again in 10, so the libraries in `lib/` must come from the bundle that matches the firmware you flashed.

**`AttributeError: 'module' object has no attribute 'PWMOut'`.** You're running an older version of this code. `PWMOut` moved from `pulseio` to `pwmio` in CircuitPython 7. The current `code.py` here already uses `pwmio`.

**No sound, or crackly sound.** Check that the white clip is on `A0 / AUDIO` and the black clip is on `GND`, and that the WAV is 16-bit mono. Stereo or 8-bit files won't play.

**A servo twitches or the board resets when servos move.** Make sure both servo power leads are on `VOUT`, not `3.3V`, and that you're on a USB supply that can deliver at least 1 A.

**The app can't find Buddy.** The board only advertises when no phone is connected. If another phone is already connected, disconnect it first. If you changed `ble.name`, toggle Bluetooth off and on so the phone forgets the cached name.

---

## Credits

Made by [Prof. John Gallaugher](https://gallaugher.com), Boston College. Buddy the Elf and the quotes belong to New Line Cinema; this is a non-commercial teaching project.

Like this? Have corrections, suggestions, or improvements? Let me know — [@gallaugher](https://bsky.app/profile/gallaugher.bsky.social).
