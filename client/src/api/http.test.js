import { beforeEach, describe, expect, it, vi } from 'vitest'
import { request, setAccessToken } from './http.js'

function jsonResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: vi.fn().mockResolvedValue(body),
  }
}

describe('api request', () => {
  beforeEach(() => {
    localStorage.clear()
    setAccessToken('')
    vi.restoreAllMocks()
  })

  it('adds json and auth headers', async () => {
    setAccessToken('token')
    const fetch = vi.fn().mockResolvedValue(jsonResponse({ ok: true }))
    vi.stubGlobal('fetch', fetch)

    await request('/api/test', {
      method: 'POST',
      body: JSON.stringify({ title: 'Idea' }),
    })

    expect(fetch).toHaveBeenCalledWith(
      'http://127.0.0.1:8000/api/test',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          Authorization: 'Bearer token',
          'Content-Type': 'application/json',
        }),
      })
    )
  })

  it('refreshes token after 401 and repeats request', async () => {
    localStorage.setItem('refresh_token', 'refresh')
    setAccessToken('old')

    const fetch = vi
      .fn()
      .mockResolvedValueOnce(jsonResponse({ detail: 'expired' }, 401))
      .mockResolvedValueOnce(jsonResponse({ access_token: 'new' }))
      .mockResolvedValueOnce(jsonResponse({ ok: true }))
    vi.stubGlobal('fetch', fetch)

    const data = await request('/api/private')

    expect(data).toEqual({ ok: true })
    expect(localStorage.getItem('access_token')).toBe('new')
    expect(fetch).toHaveBeenCalledTimes(3)
  })

  it('throws api error detail', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse({ detail: 'Bad request' }, 400)))

    await expect(request('/api/bad')).rejects.toThrow('Bad request')
  })
})
