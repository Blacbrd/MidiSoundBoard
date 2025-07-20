import mido

port_name = "DMK25 0"

with mido.open_input(port_name) as inport:

    print("Listening for MIDI...")

    for msg in inport:

        if msg.type == "note_on":

            if msg.note == 60:
                print("C")
            
            elif msg.note == 61:
                print("C#")
