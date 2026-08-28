const configuredApiUrl = import.meta.env.VITE_API_URL as string | undefined;

const deployedApiUrl = "https://neelastack.onrender.com";
const localApiUrl = "http://127.0.0.1:8000";

const isLocalHost =
  typeof window !== "undefined" &&
  (window.location.hostname === "localhost" ||
   window.location.hostname === "127.0.0.1");

export const API_BASE_URL =
  configuredApiUrl?.trim()
    ? configuredApiUrl.replace(/\/+$/, "")
    : isLocalHost
      ? localApiUrl
      : deployedApiUrl;
