from __future__ import annotations

from pathlib import Path

from openai import OpenAI


class OpenAIVoicePipeline:
    def __init__(self, stt_model: str, tts_model: str, voice: str) -> None:
        self.client = OpenAI()
        self.stt_model = stt_model
        self.tts_model = tts_model
        self.voice = voice

    def transcribe(self, wav_path: str | Path) -> str:
        wav_path = Path(wav_path)
        with wav_path.open("rb") as f:
            tx = self.client.audio.transcriptions.create(
                model=self.stt_model,
                file=f,
                response_format="text",
            )
        # SDK pode retornar string direta em alguns formatos
        return tx if isinstance(tx, str) else str(tx)

    def synthesize(
        self,
        text: str,
        output_wav_path: str | Path,
        speed: float,
        expressivity: str,
    ) -> Path:
        output_wav_path = Path(output_wav_path)
        output_wav_path.parent.mkdir(parents=True, exist_ok=True)

        styled_input = (
            f"Estilo de fala: {expressivity}. "
            f"Entregue com prosódia natural e pausas orgânicas. Texto: {text}"
        )

        with self.client.audio.speech.with_streaming_response.create(
            model=self.tts_model,
            voice=self.voice,
            input=styled_input,
            response_format="wav",
            speed=speed,
        ) as response:
            response.stream_to_file(str(output_wav_path))

        return output_wav_path
