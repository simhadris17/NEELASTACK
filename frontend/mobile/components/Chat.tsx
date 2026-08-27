import React, { useState } from "react";
import { ActivityIndicator, Button, Text, TextInput, View } from "react-native";
import { useChat } from "../hooks/useChat";

export default function Chat({ token }: { token: string }) {
  const [message, setMessage] = useState("");
  const { answer, loading, error, send } = useChat(token);
  return <View>
    <TextInput multiline placeholder="Ask NEELASTACK..." value={message} onChangeText={setMessage} />
    {loading ? <ActivityIndicator /> : <Button title="Send" onPress={() => { void send(message); setMessage(""); }} />}
    {!!answer && <Text>{answer}</Text>}
    {!!error && <Text>{error}</Text>}
  </View>;
}
