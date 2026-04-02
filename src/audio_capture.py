from __future__ import annotations

import time
import wave
from dataclasses import dataclass
from pathlib import Path

import pyaudio


@dataclass
class CaptureConfig:
    sample_rate: int = 48_000
    channels: int = 1
    sample_width_bytes: int = 3  # 24-bit PCM
    chunk_size: int = 1024
    seconds: int = 5


def record_wav(output_path: str | Path, config: CaptureConfig) -> Path:
    """Captura áudio do microfone em WAV PCM mono (24-bit por padrão)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=pyaudio.paInt24 if config.sample_width_bytes == 3 else pyaudio.paInt16,
        channels=config.channels,
        rate=config.sample_rate,
        input=True,
        frames_per_buffer=config.chunk_size,
    )

    print(f"[captura] Gravando por {config.seconds}s...")
    frames: list[bytes] = []

    total_chunks = int(config.sample_rate / config.chunk_size * config.seconds)
    start = time.time()

    for _ in range(total_chunks):
        frames.append(stream.read(config.chunk_size, exception_on_overflow=False))

    elapsed = time.time() - start
    print(f"[captura] Finalizado em {elapsed:.2f}s")

    stream.stop_stream()
    stream.close()
    pa.terminate()

    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(config.sample_width_bytes)
        wf.setframerate(config.sample_rate)
        wf.writeframes(b"".join(frames))

    print(f"[captura] Arquivo salvo: {output_path}")
    return output_path
