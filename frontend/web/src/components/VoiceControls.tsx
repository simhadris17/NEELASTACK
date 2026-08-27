import { useEffect, useRef, useState } from "react";

type Props = { onTranscript: (text: string) => void; speakText?: string };
type Recognition = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  onresult: ((event: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null;
  onend: (() => void) | null;
  onerror: (() => void) | null;
};
type RecognitionConstructor = new () => Recognition;

declare global {
  interface Window {
    SpeechRecognition?: RecognitionConstructor;
    webkitSpeechRecognition?: RecognitionConstructor;
  }
}

export default function VoiceControls({ onTranscript, speakText }: Props) {
  const recognition = useRef<Recognition | null>(null);
  const [listening, setListening] = useState(false);
  const supported = typeof window !== "undefined" &&
    Boolean(window.SpeechRecognition || window.webkitSpeechRecognition);

  useEffect(() => () => recognition.current?.stop(), []);

  function toggleListening() {
    if (!supported) return;
    if (listening) {
      recognition.current?.stop();
      setListening(false);
      return;
    }
    const Constructor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Constructor) return;
    const instance = new Constructor();
    instance.continuous = false;
    instance.interimResults = false;
    instance.lang = "en-US";
    instance.onresult = (event) => {
      const transcript = event.results[0]?.[0]?.transcript;
      if (transcript) onTranscript(transcript);
    };
    instance.onend = () => setListening(false);
    instance.onerror = () => setListening(false);
    recognition.current = instance;
    instance.start();
    setListening(true);
  }

  function speak() {
    if (speakText && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(new SpeechSynthesisUtterance(speakText));
    }
  }

  return (
    <div className="voice-controls" aria-label="Voice controls">
      <button className="secondary-button" type="button" onClick={toggleListening} disabled={!supported}>
        {listening ? "Stop listening" : "Voice input"}
      </button>
      <button className="secondary-button" type="button" onClick={speak} disabled={!speakText}>
        Read response
      </button>
      {!supported && <span className="voice-hint">Browser speech input unavailable</span>}
    </div>
  );
}
