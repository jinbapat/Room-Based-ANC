"""
room_simulation.py — Virtual room modeling using pyroomacoustics
Phase 1 — Room-Based ANC
"""

import numpy as np
import pyroomacoustics as pra


def create_room(
    room_dim=(4, 3, 2.5),
    fs=16000,
    absorption=0.3,
    max_order=10,
):
    """
    Create a shoebox room model with given dimensions and acoustic properties.
    Returns the room object.
    """
    room = pra.ShoeBox(
        p=room_dim,
        fs=fs,
        materials=pra.Material(absorption),
        max_order=max_order,
    )
    return room


def add_sources_and_mics(room, noise_src_pos, spkr_pos, mic_pos):
    """
    Add noise source, control speaker, and microphones to the room.
    """
    room.add_source(noise_src_pos)  # noise source
    room.add_source(spkr_pos)       # control speaker
    room.add_microphone_array(np.c_[mic_pos])  # error mic (for now single)
    return room


def simulate_ir(room):
    """
    Compute impulse responses for all source-microphone pairs.
    Returns dictionary with IRs for primary and secondary paths.
    """
    room.compute_rir()

    n_sources = len(room.sources)
    n_mics = room.mic_array.R.shape[1]
    print(f"Computed RIRs for {n_sources} sources and {n_mics} mic(s).")

    # Debug: list RIR lengths
    for i, src_rirs in enumerate(room.rir):
        for j, rir in enumerate(src_rirs):
            print(f"RIR source {i} → mic {j}: {len(rir)} samples")

    # Handle cases gracefully
    rir_primary = room.rir[0][0] if len(room.rir) > 0 and len(room.rir[0]) > 0 else np.zeros(256)
    rir_secondary = (
        room.rir[1][0]
        if len(room.rir) > 1 and len(room.rir[1]) > 0
        else np.zeros(256)
    )

    return {
        "primary": np.array(rir_primary),
        "secondary": np.array(rir_secondary),
    }


def simulate_room_paths(fs=16000):
    """
    High-level function:
    Builds room, adds sources/mic, computes and returns impulse responses.
    """
    room = create_room(fs=fs)
    noise_src_pos = [1.0, 1.0, 1.5]
    spkr_pos = [3.0, 2.5, 1.2]
    mic_pos = [2.0, 1.5, 1.2]

    room = add_sources_and_mics(room, noise_src_pos, spkr_pos, mic_pos)
    irs = simulate_ir(room)
    return irs
