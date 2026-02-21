import { defineStore } from "pinia";

export const useAppStore = defineStore(
  "app",
  () => {
    const fetchJSON = async (url, timeoutMs = 20000) => {
      const controller = new AbortController();
      const signal = controller.signal;
      const id = setTimeout(() => controller.abort(), timeoutMs);

      try {
        const response = await fetch(url, { method: "GET", signal });
        if (!response.ok) {
          const text = await response.text();
          console.log("API non-OK:", response.status, text);
          return { status: "failed", data: [] };
        }

        const json = await response.json();
        return json;
      } catch (err) {
        console.error("fetchJSON error:", err?.message || err);
        return { status: "failed", data: [] };
      } finally {
        clearTimeout(id);
      }
    };

    const unwrapData = (json) => {
      if (!json || typeof json !== "object") return [];
      const st = json.status;
      if (st === "found" || st === "ok") {
        return Array.isArray(json.data) ? json.data : [];
      }
      return [];
    };

    const getAllInRange = async (start, end) => {
      const url = `/api/climo/get/${start}/${end}`;
      const json = await fetchJSON(url, 60000);
      return unwrapData(json);
    };

    const getTemperatureMMAR = async (start, end) => {
      const url = `/api/mmar/temperature/${start}/${end}`;
      const json = await fetchJSON(url);
      return unwrapData(json);
    };

    const getHumidityMMAR = async (start, end) => {
      const url = `/api/mmar/humidity/${start}/${end}`;
      const json = await fetchJSON(url);
      return unwrapData(json);
    };

    const getFreqDistro = async (variable, start, end) => {
      const url = `/api/frequency/${variable}/${start}/${end}`;
      const json = await fetchJSON(url, 60000);
      return unwrapData(json);
    };

    return {
      getAllInRange,
      getTemperatureMMAR,
      getHumidityMMAR,
      getFreqDistro,
    };
  },
  { persist: true }
);
