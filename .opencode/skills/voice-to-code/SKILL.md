---
name: voice-to-code
description: Use when converting spoken language to code, transcribing voice commands, or when the user wants to dictate code. Trigger on phrases like "voice input", "dictate", "speak", "transcribe", "voice command", "speech to code", or when audio transcription is needed.
---

# Voice-to-Code Skill

Convert spoken language into code and commands.

## How It Works

```
User speaks → Transcription → Natural language → Code generation
```

## Transcription Tools

### Using Whisper (OpenAI)
```bash
# Install whisper
pip install openai-whisper --break-system-packages

# Transcribe audio file
whisper audio.wav --language en --model base

# Transcribe with timestamps
whisper audio.wav --output_format txt --output_dir /tmp/
```

### Using Vosk (Offline)
```bash
# Install vosk
pip install vosk --break-system-packages

# Download model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### Using Google Speech Recognition
```bash
# Install SpeechRecognition
pip install SpeechRecognition --break-system-packages

# Transcribe from microphone
python3 -c "
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('Speak now...')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f'You said: {text}')
    except sr.UnknownValueError:
        print('Could not understand audio')
"
```

## Voice Command Patterns

### Natural Language to Code

| User Says | Generated Code |
|-----------|---------------|
| "Calculate sine of 45 degrees" | `engine.calculate("sin(45)", angle_mode="degrees")` |
| "Convert 100 USD to EUR" | `convert(100, "USD", "EUR")` |
| "Plot y equals x squared" | `plot("x**2", -10, 10)` |
| "What's 15 percent of 200" | `engine.calculate("200 * 0.15")` |
| "Run the tests" | `python -m pytest tests/ -x -q` |

### Command Patterns

| User Says | Action |
|-----------|--------|
| "Open file engine.py" | Read `core/engine.py` |
| "Run tests" | Execute test suite |
| "Commit changes" | Git commit |
| "Show me the graph" | Open browser to localhost:5000 |

## Implementation

```python
# voice_assistant.py
import speech_recognition as sr
from core.engine import MathEngine

class VoiceCalculator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = MathEngine()

    def listen(self) -> str:
        """Listen for voice command."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio)

    def process(self, command: str) -> str:
        """Convert voice command to action."""
        # Map natural language to calculator functions
        command = command.lower()

        if "calculate" in command or "compute" in command:
            expr = self.extract_expression(command)
            result = self.engine.calculate(expr)
            return f"Result: {result}"

        if "convert" in command:
            # Handle unit conversion
            pass

        if "plot" in command or "graph" in command:
            # Handle graphing
            pass

        return "Command not recognized"

    def extract_expression(self, command: str) -> str:
        """Extract math expression from natural language."""
        # Simple pattern matching
        import re

        # "sine of 45 degrees" → "sin(45 * pi / 180)"
        match = re.search(r'sine of (\d+)', command)
        if match:
            return f"sin({match.group(1)} * pi / 180)"

        # "square root of 144" → "sqrt(144)"
        match = re.search(r'square root of (\d+)', command)
        if match:
            return f"sqrt({match.group(1)})"

        # "15 percent of 200" → "200 * 0.15"
        match = re.search(r'(\d+) percent of (\d+)', command)
        if match:
            return f"{match.group(2)} * {int(match.group(1))/100}"

        return command

    def run(self):
        """Main voice loop."""
        print("Voice Calculator ready. Say 'quit' to exit.")
        while True:
            try:
                text = self.listen()
                print(f"You said: {text}")

                if "quit" in text or "exit" in text:
                    break

                response = self.process(text)
                print(response)

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    VoiceCalculator().run()
```

## Integration with opencode

```bash
# Add voice command alias
alias vcalc='python3 /home/mulugeta/projects/multi_mode_calculator/voice_assistant.py'

# Or integrate with opencode via custom command
cat > ~/.config/opencode/command/voice.md << 'EOF'
---
description: Process voice input for calculator
---

Listen for voice input and convert to calculator command.

1. Activate microphone
2. Transcribe speech
3. Parse natural language
4. Execute calculator function
5. Return result as speech
EOF
```

## Rules

- Always confirm transcription before executing
- Provide text fallback for all voice commands
- Handle background noise gracefully
- Support common accents and speech patterns
- Log voice commands for debugging
- Never execute dangerous commands from voice input
