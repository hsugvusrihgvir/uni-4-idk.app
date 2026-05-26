import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../api/telegram.js', () => ({
  createTelegramLinkCode: vi.fn(),
}))

import * as telegramApi from '../api/telegram.js'
import { useStore } from './store.js'

describe('store telegram actions', () => {
  beforeEach(() => {
    useStore().state.error = ''
    vi.clearAllMocks()
  })

  it('returns telegram link code', async () => {
    telegramApi.createTelegramLinkCode.mockResolvedValue({ code: '123456' })

    await expect(useStore().createTelegramLinkCode()).resolves.toBe('123456')
  })

  it('stores request error if telegram code request fails', async () => {
    telegramApi.createTelegramLinkCode.mockRejectedValue(new Error('server down'))

    await expect(useStore().createTelegramLinkCode()).rejects.toThrow('server down')
    expect(useStore().state.error).toBe('server down')
  })
})
