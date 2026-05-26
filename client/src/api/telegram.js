import { request } from './http.js'

export function createTelegramLinkCode() {
  return request('/api/v1/telegram/link-code', {
    method: 'POST',
  })
}
