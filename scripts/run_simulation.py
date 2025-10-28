import os
import numpy as np 

def main():
    print("Room-Based ANC - Phase 1 Simulation")
    os.makedirs("../outputs", exist_ok=True)

    duration = 2.0 # seconds
    fs = 16000  # Hz
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    noise = np.random.normal(0, 1, t.shape)
    
    print(f"Generated white noise of duration {duration} seconds at {fs} Hz sampling rate.")

if __name__ == "__main__":
    main()

from src.simulation import signal_utils as su

fs = 16000
duration = 2.0

white = su.generate_white_noise(duration, fs)
pink = su.generate_pink_noise(duration, fs)
tone = su.generate_sine(440, duration, fs)

'''
su.save_audio("../outputs/test_white.wav", white, fs)
su.save_audio("../outputs/test_pink.wav", pink, fs)
su.save_audio("../outputs/test_sine.wav", tone, fs)

print("Saved test noise signals in outputs/.")
'''

from src.simulation import room_sim as rs

irs = rs.simulate_room_paths(fs)
print(f"Primary IR length: {len(irs['primary'])}")
print(f"Secondary IR length: {len(irs['secondary'])}")

# Optional: save them for inspection
import soundfile as sf
sf.write("../outputs/rir_primary.wav", irs["primary"], fs)
sf.write("../outputs/rir_secondary.wav", irs["secondary"], fs)

print("Saved room impulse responses to outputs/.")
