# Aplicativo de Voz com OpenAI (STT + TTS) — 48 kHz / 24-bit WAV PCM mono

Este projeto implementa um pipeline de voz em **baixa latência** com foco em uso real em **ambiente coletivo**:

- Entrada principal por **texto escrito** (padrão);
- Captura de áudio opcional em **48.000 Hz**, **24 bits**, **WAV PCM linear**, **mono**;
- Transcrição com Speech-to-Text da OpenAI quando usar entrada de áudio;
- Síntese com Text-to-Speech neural da OpenAI;
- Controles de **velocidade**, **pitch** e **expressividade**;
- Reprodução opcional (desativável para não atrapalhar outras pessoas no local).

> Observação: em vários fluxos de TTS, o pitch não é um controle nativo direto da API. Neste projeto ele é ajustado localmente com `ffmpeg`.

## Requisitos

- Python 3.10+
- `ffmpeg` instalado (para ajuste de pitch)
- `OPENAI_API_KEY` configurada

```bash
export OPENAI_API_KEY="sua_chave"
```

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Modos de entrada

- `--input-mode text` (padrão): usa texto digitado/arquivo/string.
- `--input-mode audio`: grava microfone em 48kHz/24-bit mono e transcreve.
- `--input-mode hybrid`: usa texto se disponível; caso não tenha, grava áudio e transcreve.

## Exemplos

### 1) Uso principal (texto escrito, recomendado em ambiente coletivo)

```bash
python app.py \
  --input-mode text \
  --text "Bom dia, equipe. A reunião começa em 10 minutos." \
  --tts-model gpt-4o-mini-tts \
  --voice alloy \
  --speed 1.03 \
  --expressivity "tom profissional, claro e cordial" \
  --no-play
```

### 2) Texto vindo de arquivo

```bash
python app.py --input-mode text --text-file ./mensagem.txt --no-play
```

### 3) Entrada por áudio (com transcrição STT)

```bash
python app.py \
  --input-mode audio \
  --seconds 6 \
  --stt-model gpt-4o-transcribe \
  --tts-model gpt-4o-mini-tts \
  --voice alloy \
  --speed 1.05 \
  --pitch-semitones 1.0 \
  --expressivity "fala calorosa, natural e fluida"
```


## Como executar (passo a passo)

1. **Criar e ativar ambiente virtual**

```bash
python -m venv .venv
source .venv/bin/activate
```

2. **Instalar dependências**

```bash
pip install -r requirements.txt
```

3. **Configurar chave da OpenAI**

```bash
export OPENAI_API_KEY="sua_chave"
```

4. **Executar no modo texto (recomendado)**

```bash
python app.py --input-mode text --text "Mensagem de teste" --no-play
```

5. **Executar no modo áudio (captura 48kHz/24-bit mono + STT + TTS)**

```bash
python app.py --input-mode audio --seconds 5 --voice alloy
```

6. **Executar modo híbrido (texto primeiro, áudio como fallback)**

```bash
python app.py --input-mode hybrid --text-file ./mensagem.txt --no-play
```

### Saídas geradas

Os arquivos são salvos por padrão em `./artifacts`:
- `input_48k_24b_mono.wav` (quando há gravação de áudio)
- `tts_raw.wav`
- `tts_final.wav`

### Execução rápida (one-liner)

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && export OPENAI_API_KEY="sua_chave" && python app.py --input-mode text --text "Olá" --no-play
```

## Requisitos técnicos atendidos

1. **Taxa de amostragem**: `48000` Hz
2. **Profundidade de bits**: `24` bits (configurável para 16)
3. **Formato de arquivo**: WAV
4. **Codificação**: PCM linear
5. **Canal**: Mono
6. **Modelo neural**: TTS avançado configurável
7. **Latência**: pipeline curto (entrada → STT opcional → TTS)
8. **Ajustes**: speed, pitch e expressividade

## Estrutura

- `app.py`: orquestra os modos `text`, `audio`, `hybrid`
- `src/audio_capture.py`: gravação WAV PCM mono em 48k/24-bit
- `src/pipeline.py`: STT + TTS com OpenAI API
- `src/audio_effects.py`: pitch shift por semitons com `ffmpeg`
