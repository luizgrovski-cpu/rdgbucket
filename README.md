# Aplicativo de Voz com OpenAI (STT + TTS) — 48 kHz / 24-bit WAV PCM mono

Este projeto implementa um pipeline de voz em **baixa latência** com:

- Captura de áudio do microfone em **48.000 Hz**, **24 bits**, **WAV PCM linear**, **mono**;
- Transcrição usando **Speech-to-Text** da OpenAI;
- Síntese com **Text-to-Speech neural** da OpenAI;
- Controles de **velocidade**, **pitch** e **expressividade**;
- Reprodução contínua para fluxo natural.

> Observação importante: no TTS da OpenAI, o controle direto de **pitch** pode variar conforme o endpoint/modelo. Neste projeto, o pitch é aplicado com pós-processamento local via `ffmpeg`, enquanto velocidade e expressividade são passadas à API quando disponível.

## Requisitos

- Python 3.10+
- `ffmpeg` instalado no sistema (para ajuste de pitch)
- Variável de ambiente:

```bash
export OPENAI_API_KEY="sua_chave"
```

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python app.py \
  --seconds 6 \
  --stt-model gpt-4o-transcribe \
  --tts-model gpt-4o-mini-tts \
  --voice alloy \
  --speed 1.05 \
  --pitch-semitones 1.0 \
  --expressivity "fala calorosa, natural e fluida"
```

### Parâmetros de áudio atendidos

1. **Taxa de amostragem**: `48000` Hz (premium)
2. **Profundidade de bits**: `24` bits (também suporta 16 com ajuste)
3. **Formato de arquivo**: WAV (sem perdas)
4. **Codificação**: PCM linear
5. **Canal**: Mono
6. **Modelo neural**: TTS avançado (`gpt-4o-mini-tts`, configurável)
7. **Baixa latência**: captura curta + transcrição + síntese em sequência rápida
8. **Ajustes**: speed via API e pitch/entonação via pós-processamento + instruções

## Arquitetura rápida

- `src/audio_capture.py`: grava WAV PCM mono em 48k/24-bit
- `src/pipeline.py`: STT + TTS usando OpenAI API
- `src/audio_effects.py`: ajuste de pitch por semitons com `ffmpeg`
- `app.py`: orquestra fluxo ponta a ponta

## Dicas de latência

- Grave janelas curtas (2–6s) para resposta mais rápida.
- Evite blocos muito longos antes da transcrição.
- Para conversa contínua, rode em loop e processe por blocos.
