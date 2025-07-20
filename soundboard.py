import mido
import sounddevice as sd
import soundfile as sf
from threading import Thread, Event

# print("Available audio devices:")
# for idx, dev in enumerate(sd.query_devices()):
#     print(idx, dev['name'], "(output ch:", dev['max_output_channels'], ")")

VIRTUAL_CABLE_INDEX = 5
sd.default.device = (None, VIRTUAL_CABLE_INDEX)
PORT_NAME = "DMK25 0"

SAMPLE_RATE = 44_100

soundboard = {
    60: r"C:\Users\blacb\Desktop\Soundboard\correct.mp3",
    62: r"C:\Users\blacb\Desktop\Soundboard\wrong-lie-incorrect-buzzer.mp3",
    64: r"C:\Users\blacb\Desktop\Soundboard\oh_my_god_vine.mp3",
    65: r"C:\Users\blacb\Desktop\Soundboard\ksi-lol.mp3",
    67: r"C:\Users\blacb\Desktop\Soundboard\hell-nah-dog_lU72pEf.mp3"
}

def mic_forward():
    
    MIC_INDEX = 2

    # This stream simply copies whatever comes in on your mic to the virtual cable
    def callback(indata, outdata, frames, time, status):
        if status:
            print("Mic Forward Warning:", status)
        outdata[:] = indata

    with sd.Stream(device=(MIC_INDEX, VIRTUAL_CABLE_INDEX),
                   samplerate=SAMPLE_RATE,
                   channels=1,
                   dtype='float32',
                   callback=callback):
        Event().wait()


Thread(target=mic_forward, daemon=True).start()


def play_sound(path):
    data, fs = sf.read(path, dtype='float32')
    # spawn a one‑off OutputStream so multiple clips can overlap
    stream = sd.OutputStream(device=VIRTUAL_CABLE_INDEX,
                             samplerate=fs,
                             channels=data.shape[1] if data.ndim > 1 else 1,
                             dtype='float32')
    stream.start()
    stream.write(data)
    stream.stop()
    stream.close()

def on_midi_message(msg):
    if msg.type == "note_on" and msg.velocity > 0:
        path = soundboard.get(msg.note)
        if path:
            Thread(target=play_sound, args=(path,), daemon=True).start()
            print(f"Playing {path}")

sd.default.samplerate = SAMPLE_RATE
with mido.open_input(PORT_NAME) as inport:
    print("Listening for MIDI → soundboard… (press Ctrl+C to quit)")
    for msg in inport:
        on_midi_message(msg)
