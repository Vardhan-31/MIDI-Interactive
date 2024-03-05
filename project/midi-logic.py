import mido
from pynput import keyboard

# Initialize MIDI
mido.set_backend('mido.backends.rtmidi')
output_port = mido.open_output()

# Mapping of keys to MIDI notes for Sa Re Ga Ma classical music
key_to_note = {
    'a': 60,  # Sa
    's': 62,  # Re
    'd': 64,  # Ga
    'f': 65,  # Ma
    'g': 67,  # Pa
    'h': 69,  # Dha
    'j': 71,  # Ni
    'k': 72,  # Sa (Higher Octave)
    'l': 74,
    'z': 76,
    'z': 76,
    'w': 61,
    'e': 63,
    't': 66, 
    'y': 68,
    'u': 70,
    "o": 73,
    'p': 75,
}

gm_instruments = [
   "Acoustic Grand Piano",
    "Bright Acoustic Piano",
    "Electric Grand Piano",
    "Honky-tonk Piano",
    "Electric Piano 1 (Rhodes Piano)",
    "Electric Piano 2 (Chorused Rhodes)",
    "Harpsichord",
    "Clavinet",
    "Celesta",
    "Glockenspiel",
    "Music Box",
    "Vibraphone",
    "Marimba",
    "Xylophone",
    "Tubular Bells",
    "Dulcimer",
    "Drawbar Organ",
    "Percussive Organ",
    "Rock Organ",
    "Church Organ",
    "Reed Organ",
    "Accordion",
    "Harmonica",
    "Tango Accordion",
    "Acoustic Guitar (nylon)",
    "Acoustic Guitar (steel)",
    "Electric Guitar (jazz)",
    "Electric Guitar (clean)",
    "Electric Guitar (muted)",
    "Overdriven Guitar",
    "Distortion Guitar",
    "Guitar Harmonics",
    "Acoustic Bass",
    "Electric Bass (finger)",
    "Electric Bass (pick)",
    "Fretless Bass",
    "Slap Bass 1",
    "Slap Bass 2",
    "Synth Bass 1",
    "Synth Bass 2",
    "Violin",
    "Viola",
    "Cello",
    "Contrabass",
    "Tremolo Strings",
    "Pizzicato Strings",
    "Orchestral Harp",
    "Timpani",
    "String Ensemble 1",
    "String Ensemble 2",
    "SynthStrings 1",
    "SynthStrings 2",
    "Choir Aahs",
    "Voice Oohs",
    "Synth Voice",
    "Orchestra Hit",
    "Trumpet",
    "Trombone",
    "Tuba",
    "Muted Trumpet",
    "French Horn",
    "Brass Section",
    "SynthBrass 1",
    "SynthBrass 2",
    "Soprano Sax",
    "Alto Sax",
    "Tenor Sax",
    "Baritone Sax",
    "Oboe",
    "English Horn",
    "Bassoon",
    "Clarinet",
    "Piccolo",
    "Flute",
    "Recorder",
    "Pan Flute",
    "Blown Bottle",
    "Shakuhachi",
    "Whistle",
    "Ocarina",
    "Lead 1 (square)",
    "Lead 2 (sawtooth)",
    "Lead 3 (calliope)",
    "Lead 4 (chiff)",
    "Lead 5 (charang)",
    "Lead 6 (voice)",
    "Lead 7 (fifths)",
    "Lead 8 (bass + lead)",
    "Pad 1 (new age)",
    "Pad 2 (warm)",
    "Pad 3 (polysynth)",
    "Pad 4 (choir)",
    "Pad 5 (bowed)",
    "Pad 6 (metallic)",
    "Pad 7 (halo)",
    "Pad 8 (sweep)",
    "FX 1 (rain)",
    "FX 2 (soundtrack)",
    "FX 3 (crystal)",
    "FX 4 (atmosphere)",
    "FX 5 (brightness)",
    "FX 6 (goblins)",
    "FX 7 (echoes)",
    "FX 8 (sci-fi)",
    "Sitar",
    "Banjo",
    "Shamisen",
    "Koto",
    "Kalimba",
    "Bag pipe",
    "Fiddle",
    "Shanai",
    "Tinkle Bell",
    "Agogo",
    "Steel Drums",
    "Woodblock",
    "Taiko Drum",
    "Melodic Tom",
    "Synth Drum",
    "Reverse Cymbal",
    "Guitar Fret Noise",
    "Breath Noise",
    "Seashore",
    "Bird Tweet",
    "Telephone Ring",
    "Helicopter",
    "Applause",
    "Gunshot"

]

# Function to get a subset of instruments
def get_instrument_subset(start):
    return {str(i % 10): (start + i) for i in range(10)}

# Initialize the current program and subset
current_program = 0
instrument_subset_start = 0

# Function to play a MIDI note with the specified program
def play_midi_note(note, program):
    msg_note_on = mido.Message('note_on', note=note, velocity=64, channel=0)
    msg_program_change = mido.Message('program_change', program=program, channel=0)
    output_port.send(msg_program_change)
    output_port.send(msg_note_on)

# Function to handle key press
def on_key_press(key):
    global current_program, instrument_subset_start
    try:
        char_key = key.char.lower()
        if char_key in key_to_note:
            note = key_to_note[char_key]
            play_midi_note(note, current_program)
        elif char_key.isdigit():
            current_program = get_instrument_subset(instrument_subset_start)[char_key]
        elif char_key == 'n':  # Switch to the next subset of instruments
            instrument_subset_start = (instrument_subset_start + 10) % 128
        elif char_key == 'p':  # Switch to the previous subset of instruments
            instrument_subset_start = (instrument_subset_start - 10) % 128
    except AttributeError:
        pass

# Function to stop playing a MIDI note
def stop_midi_note(note):
    msg_note_off = mido.Message('note_off', note=note, velocity=64, channel=0)
    output_port.send(msg_note_off)

# Function to handle key release
def on_key_release(key):
    try:
        char_key = key.char.lower()
        if char_key in key_to_note:
            note = key_to_note[char_key]
            stop_midi_note(note)
    except AttributeError:
        pass

# Set up keyboard listener
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        # Close the output port when the program exits
        output_port.close()
