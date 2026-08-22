export const BACKEND_URL = "http://127.0.0.1:8000"

const response = await fetch(`${BACKEND_URL}/api/version`)
const data = await response.json()

export const API_VERSION = data.version