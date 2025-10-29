# Room-Based-ANC

Room-Based-ANC implements and experiments with Active Noise Control (ANC) in realistic room environments. The project focuses on creating localized quiet zones using microphones, speakers, and adaptive digital filters while accounting for room acoustics and measured/simulated room impulse responses (RIRs).

## Highlights

- Simple, reproducible room/noise simulation utilities
- Scripts to run simulations and produce example audio outputs
- Small codebase intended for research experiments and teaching demos

## Repository structure

Top-level layout:

- `requirements.txt` — Python dependencies
- `scripts/` — runnable scripts (e.g., `run_simulation.py`)
- `src/` — library code
	- `simulation/room_sim.py` — room simulation utilities
	- `simulation/signal_utils.py` — signal helpers (windowing, synthesis, I/O)
- `outputs/` — generated audio outputs and example RIRs

Example files already present in `outputs/`:

- `rir_primary.wav`, `rir_secondary.wav` — example room impulse responses
- `test_pink.wav`, `test_sine.wav`, `test_white.wav` — test signals

## Quick start

These steps assume you are on Windows PowerShell (the repo was developed with cross-platform Python in mind):

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the simulation script

```powershell
python .\scripts\run_simulation.py
```

The script will produce output files in the `outputs/` directory. See the script docstring or comments for configurable parameters (room size, microphone/speaker layout, signals, etc.).

## How it works (brief)

1. Room and source/receiver geometry are defined in `src/simulation/room_sim.py`.
2. Room impulse responses (RIRs) are simulated or loaded from `outputs/`.
3. Signals are generated or loaded (`src/simulation/signal_utils.py`) and passed through the acoustic paths.
4. Adaptive control logic is implemented as experiments — the project is structured to make it easy to swap algorithms and evaluation metrics.

## Examples / Outputs

- `outputs/test_sine.wav` — simple tone used to verify signal routing
- `outputs/test_white.wav` / `outputs/test_pink.wav` — broadband test signals
- `outputs/rir_primary.wav` / `outputs/rir_secondary.wav` — example RIRs that the simulation uses

Open these files in any audio player or use Python to load and inspect them (e.g., `scipy.io.wavfile` or `soundfile`).

## Development notes

- Code is small and intended for experimentation. If you add algorithms or modules, please add unit tests and document usage in this README.
- Follow the existing code style; keep I/O separated from core algorithm logic to ease testing.

## Contributing

Contributions are welcome. Please open an issue for larger changes, and submit a pull request with a clear description and minimal, focused commits.

## License

This repository includes a `LICENSE` file at the project root. Check it for licensing details.

## Contact

Project owner: `jinbapat` (see repository on GitHub). For questions or suggestions, open an issue on the repo.



