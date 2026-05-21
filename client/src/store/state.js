export const baseState = {
  auth: {
    user: null,
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
  },
  boards: [],
  ideas: [],
  votings: {},
  voteResults: {},
  notifications: [],
  ws: {},
  loading: false,
  error: '',
}
