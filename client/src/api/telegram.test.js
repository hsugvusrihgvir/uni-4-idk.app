import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createTelegramLinkCode } from './telegram.js'
import { setAccessToken } from './http.js'

function jsonResponse(body) {
  return {
    ok: true,
    status: 200,
    json: vi.fn().mockResolvedValue(body),
  }
}

describe('telegram api', () => {
  beforeEach(() => {
    localStorage.clear()
    setAccessToken('token')
    vi.restoreAllMocks()
  })

  it('requests telegram link code', async () => {
    const fetch = vi.fn().mockResolvedValue(jsonResponse({ code: '123456' }))
    vi.stubGlobal('fetch', fetch)

    const data = await createTelegramLinkCode()

    expect(data).toEqual({ code: '123456' })
    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/v1/telegram/link-code',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          Authorization: 'Bearer token',
        }),
      })
    )
  })
})
