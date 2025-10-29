"""
room_simulation.py — Virtual room modeling using pyroomacoustics
Phase 1 — Room-Based ANC
"""

import numpy as np
import pyroomacoustics as pra
import os
import soundfile as sf
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# 1. Room creation
# -----------------------------------------------------------

def create_room(
    room_dim=(4, 3, 2.5),
    fs=16000,
    absorption=0.15,
    max_order=25,
):
    """
    Create a shoebox room model for ANC simulation.

    Lower absorption + higher max_order → longer impulse responses.
    """
    return pra.ShoeBox(
        p=room_dim,
        fs=fs,
        materials=pra.Material(absorption),
        max_order=max_order,
    )


# -----------------------------------------------------------
# 2. Utility: zero-pad to fixed time length
# -----------------------------------------------------------

def pad_ir(ir, fs, target_time_s=0.3):
    """
    Pad or truncate an IR to a fixed duration (seconds).
    Default = 0.3s @ fs.
    """
    ir = np.array(ir)
    target_len = int(target_time_s * fs)
    if len(ir) < target_len:
        ir = np.pad(ir, (0, target_len - len(ir)))
    else:
        ir = ir[:target_len]
    return ir


# -----------------------------------------------------------
# 3. Add sources and mic
# -----------------------------------------------------------

def add_sources_and_mics(room, noise_src_pos, spkr_pos, mic_pos):
    """
    Add microphones first, then noise and speaker sources.
    """
    mic_pos = np.atleast_2d(mic_pos).T
    room.add_microphone_array(pra.MicrophoneArray(mic_pos, room.fs))

    room.add_source(noise_src_pos)  # noise source
    room.add_source(spkr_pos)       # control speaker
    return room



# -----------------------------------------------------------
# 4. Compute IRs
# -----------------------------------------------------------

def compute_irs(room, fs, target_time_s=0.3, save_dir=None, plot=False):
    """
    Compute RIRs for primary (noise→mic) and secondary (speaker→mic) paths.
    """

    room.compute_rir()

    # Debug: visualize structure
    print("RIR structure:", [[len(r) for r in src] for src in room.rir])

    # Safely extract IRs
    rir_primary = np.array(room.rir[0][0]) if len(room.rir) > 0 and len(room.rir[0]) > 0 else np.zeros(int(target_time_s * fs))
    rir_secondary = np.array(room.rir[1][0]) if len(room.rir) > 1 and len(room.rir[1]) > 0 else np.zeros(int(target_time_s * fs))

    rir_primary = pad_ir(rir_primary, fs, target_time_s)
    rir_secondary = pad_ir(rir_secondary, fs, target_time_s)

    print(f"Primary IR length: {len(rir_primary)}")
    print(f"Secondary IR length: {len(rir_secondary)}")

    if save_dir is not None:
        os.makedirs(save_dir, exist_ok=True)
        sf.write(os.path.join(save_dir, "rir_primary.wav"), rir_primary, fs)
        sf.write(os.path.join(save_dir, "rir_secondary.wav"), rir_secondary, fs)
        print(f"Saved RIRs to {save_dir}")

    if plot:
        plt.figure(figsize=(10, 4))
        plt.plot(rir_primary, label="Primary IR")
        plt.plot(rir_secondary, label="Secondary IR", alpha=0.8)
        plt.title("Room Impulse Responses")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.show()

    return {"primary": rir_primary, "secondary": rir_secondary}

# -----------------------------------------------------------
# 5. High-level pipeline entry
# -----------------------------------------------------------

def simulate_room_paths(fs=16000, save_dir=None, plot=False):
    """
    High-level function:
    Builds a small virtual room, places mic + sources,
    and computes IRs for ANC simulation.
    """
    room = create_room(fs=fs)

    # Define positions (in meters)
    noise_src_pos = [0.5, 1.0, 1.5]   # primary noise source
    spkr_pos = [3.5, 2.5, 1.2]        # control speaker
    mic_pos = [2.0, 1.5, 1.2]         # error mic / listener

    room = add_sources_and_mics(room, noise_src_pos, spkr_pos, mic_pos)

    irs = compute_irs(
        room,
        fs=fs,
        target_time_s=0.3,   # 300 ms IR
        save_dir=save_dir,
        plot=plot,
    )

    return irs
