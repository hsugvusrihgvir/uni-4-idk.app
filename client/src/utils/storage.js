export const STORAGE_KEY = 'aura-board-clean-state-v1'

export function loadState(defaultState) {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : structuredClone(defaultState)
  } catch {
    return structuredClone(defaultState)
  }
}

export function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}

export function resetState() {
  localStorage.removeItem(STORAGE_KEY)
}
