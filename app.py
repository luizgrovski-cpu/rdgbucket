from __future__ import annotations

import argparse
from pathlib import Path

import simpleaudio as sa
from dotenv import load_dotenv

from src.audio_capture import CaptureConfig, record_wav
from src.audio_effects import apply_pitch_shift_ffmpeg
from src.pipeline import OpenAIVoicePipeline


INPUT_MODES = ("text", "audio", "hybrid")


def play_wav(path: str | Path) -> None:
    wave_obj = sa.WaveObject.from_wave_file(str(path))
    play_obj = wave_obj.play()
    play_obj.wait_done()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Pipeline STT + TTS com OpenAI")
    p.add_argument("--input-mode", choices=INPUT_MODES, default="text")
    p.add_argument("--text", default="")
    p.add_argument("--text-file", default="")
    p.add_argument("--seconds", type=int, default=5)
    p.add_argument("--stt-model", default="gpt-4o-transcribe")
    p.add_argument("--tts-model", default="gpt-4o-mini-tts")
    p.add_argument("--voice", default="alloy")
    p.add_argument("--speed", type=float, default=1.0)
    p.add_argument("--pitch-semitones", type=float, default=0.0)
    p.add_argument("--expressivity", default="voz clara, amigável e natural")
    p.add_argument("--workdir", default="./artifacts")
    p.add_argument(
        "--no-play",
        action="store_true",
        help="Não reproduz áudio localmente (recomendado em ambiente coletivo).",
    )
    return p


def load_text_input(raw_text: str, text_file: str, prompt_if_empty: bool = True) -> str:
    if raw_text.strip():
        return raw_text.strip()
    if text_file.strip():
        return Path(text_file).read_text(encoding="utf-8").strip()
    if not prompt_if_empty:
        return ""

    print("[input] Digite o texto e pressione Enter:")
    return input().strip()


def resolve_text(args: argparse.Namespace, pipeline: OpenAIVoicePipeline, raw_wav: Path) -> str:
    if args.input_mode == "text":
        return load_text_input(args.text, args.text_file)

    if args.input_mode == "audio":
        record_wav(
            raw_wav,
            CaptureConfig(sample_rate=48_000, channels=1, sample_width_bytes=3, seconds=args.seconds),
        )
        return pipeline.transcribe(raw_wav)

    # hybrid: usa texto se existir; se estiver vazio, cai para áudio
    text = load_text_input(args.text, args.text_file, prompt_if_empty=False)
    if text:
        return text

    record_wav(
        raw_wav,
        CaptureConfig(sample_rate=48_000, channels=1, sample_width_bytes=3, seconds=args.seconds),
    )
    return pipeline.transcribe(raw_wav)


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()

    workdir = Path(args.workdir)
    raw_wav = workdir / "input_48k_24b_mono.wav"
    tts_wav = workdir / "tts_raw.wav"
    final_wav = workdir / "tts_final.wav"

    pipeline = OpenAIVoicePipeline(
        stt_model=args.stt_model,
        tts_model=args.tts_model,
        voice=args.voice,
    )

    text = resolve_text(args, pipeline, raw_wav)
    if not text:
        raise ValueError("Nenhum texto informado/capturado para sintetizar.")

    print(f"[input] Texto final: {text}")

    pipeline.synthesize(
        text=text,
        output_wav_path=tts_wav,
        speed=args.speed,
        expressivity=args.expressivity,
    )

    if abs(args.pitch_semitones) > 0.001:
        apply_pitch_shift_ffmpeg(tts_wav, final_wav, args.pitch_semitones)
    else:
        final_wav = tts_wav

    print(f"[tts] Saída gerada em: {final_wav}")

    if not args.no_play:
        print(f"[tts] Reprodução: {final_wav}")
        play_wav(final_wav)


if __name__ == "__main__":
    main()
