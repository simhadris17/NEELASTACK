import React, { useState } from "react";
import { ActivityIndicator, Button, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { api, login, register } from "./services/api";

export default function App() {
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function authenticate(action: "login" | "register") {
    setBusy(true); setError("");
    try {
      setToken(action === "login" ? await login(email, password) : await register(email, password));
    } catch (e) { setError(e instanceof Error ? e.message : "Authentication failed"); }
    finally { setBusy(false); }
  }

  async function send() {
    if (!message.trim() || !token) return;
    setBusy(true); setError("");
    try { setAnswer((await api<{ answer: string }>("/api/v1/chat", { method: "POST", token, body: { message } })).answer); setMessage(""); }
    catch (e) { setError(e instanceof Error ? e.message : "Chat request failed"); }
    finally { setBusy(false); }
  }

  if (!token) return (
    <SafeAreaView style={styles.container}><Text style={styles.title}>NEELASTACK</Text>
      <Text style={styles.subtitle}>Local-first AI platform</Text>
      <TextInput autoCapitalize="none" keyboardType="email-address" placeholder="Email" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput secureTextEntry placeholder="Password" value={password} onChangeText={setPassword} style={styles.input} />
      {busy ? <ActivityIndicator /> : <View style={styles.buttons}><Button title="Sign in" onPress={() => authenticate("login")} /><Button title="Create account" onPress={() => authenticate("register")} /></View>}
      {!!error && <Text style={styles.error}>{error}</Text>}
    </SafeAreaView>
  );
  return <SafeAreaView style={styles.container}><ScrollView>
    <Text style={styles.title}>Chat</Text><Text style={styles.subtitle}>Connected to the same /api/v1 API</Text>
    <TextInput multiline placeholder="Ask NEELASTACK..." value={message} onChangeText={setMessage} style={[styles.input, styles.message]} />
    {busy ? <ActivityIndicator /> : <Button title="Send" onPress={send} />}
    {!!answer && <View style={styles.answer}><Text>{answer}</Text></View>}
    {!!error && <Text style={styles.error}>{error}</Text>}
    <Button title="Sign out" onPress={() => setToken(null)} />
  </ScrollView></SafeAreaView>;
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", backgroundColor: "#f8fafc" },
  title: { fontSize: 30, fontWeight: "700", marginBottom: 6, color: "#111827" },
  subtitle: { color: "#64748b", marginBottom: 24 },
  input: { backgroundColor: "white", borderColor: "#cbd5e1", borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 12 },
  message: { minHeight: 110, textAlignVertical: "top" },
  buttons: { gap: 12 },
  answer: { backgroundColor: "white", borderRadius: 8, padding: 16, marginVertical: 20 },
  error: { color: "#b91c1c", marginVertical: 12 },
});
