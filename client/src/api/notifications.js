import { request } from './http.js'

export function getNotifications() {
  return request('/api/v1/notifications')
}

export function deleteNotification(notificationId) {
  return request(`/api/v1/notifications/${notificationId}`, {
    method: 'DELETE',
  })
}
