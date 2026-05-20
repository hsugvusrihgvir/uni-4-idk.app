export const defaultState = {
  auth: {
    user: null,
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
  },
  boards: [],
  ideas: [],
  loading: false,
  error: '',
}
