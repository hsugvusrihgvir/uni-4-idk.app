import { vi } from 'vitest'

const storage = new Map()

vi.stubGlobal('localStorage', {
  getItem: vi.fn((key) => storage.get(key) || null),
  setItem: vi.fn((key, value) => storage.set(key, String(value))),
  removeItem: vi.fn((key) => storage.delete(key)),
  clear: vi.fn(() => storage.clear()),
})
