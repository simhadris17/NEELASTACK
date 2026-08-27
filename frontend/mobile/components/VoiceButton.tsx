import React from "react";
import { Button } from "react-native";

type Props = { onPress?: () => void; disabled?: boolean };

/** Recorder UI hook point; native recording can upload multipart audio to /voice/transcribe. */
export default function VoiceButton({ onPress, disabled }: Props) {
  return <Button title="Voice" onPress={onPress} disabled={disabled} />;
}
