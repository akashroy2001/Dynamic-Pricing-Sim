import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export const getConfig = () => axios.get(`${API}/config`).then((r) => r.data);
export const getForecast = () => axios.get(`${API}/forecast`).then((r) => r.data);
export const getPace = (scenario) => axios.post(`${API}/pace`, scenario).then((r) => r.data);
export const recommend = (scenario) => axios.post(`${API}/recommend`, scenario).then((r) => r.data);
export const explain = (scenario, optimization, simulation, force = false) =>
  axios.post(`${API}/explain`, { scenario, optimization, simulation, force }).then((r) => r.data);
export const saveRun = (payload) => axios.post(`${API}/runs`, payload).then((r) => r.data);
export const listRuns = () => axios.get(`${API}/runs`).then((r) => r.data);
export const getWarningLog = () => axios.get(`${API}/warnings/log`).then((r) => r.data);

export const inr = (n) => `₹${Math.round(n ?? 0).toLocaleString("en-IN")}`;
export const lakhs = (n) => `₹${((n ?? 0) / 100000).toFixed(2)} L`;
export const pct = (x, d = 0) => `${((x ?? 0) * 100).toFixed(d)}%`;
