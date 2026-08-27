# NEELASTACK Mobile

Expo client using the same REST API as the web application. Set
`EXPO_PUBLIC_API_URL` to a reachable API URL (a physical device cannot use
`127.0.0.1` for a host computer), then run `npm install` and `npx expo start`.
Authentication is kept in memory in this minimal scaffold; use Expo SecureStore
before shipping a production build. Voice endpoints are available at
`/api/v1/voice/transcribe` and `/api/v1/voice/synthesize` for a future recorder UI.
