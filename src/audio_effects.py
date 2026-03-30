from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def apply_pitch_shift_ffmpeg(input_wav: str | Path, output_wav: str | Path, semitones: float) -> Path:
    """
    Ajusta pitch em semitons usando ffmpeg.

    Para manter duração natural, usa filtro rubberband quando disponível.
    """
    input_wav = Path(input_wav)
    output_wav = Path(output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_bin = shutil.which("ffmpeg")
    if ffmpeg_bin is None:
        raise RuntimeError("ffmpeg não encontrado no PATH.")

    ratio = 2 ** (semitones / 12.0)
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i",
        str(input_wav),
        "-af",
        f"rubberband=pitch={ratio}",
        str(output_wav),
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_wav
