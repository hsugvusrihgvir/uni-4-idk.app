import { computed, reactive } from 'vue'
import { baseState } from './state.js'
import { saveTokens, clearTokens } from '../utils/storage.js'
import { setAccessToken } from '../api/http.js'
import * as auth from '../api/auth.js'
import * as users from '../api/users.js'
import * as boardReq from '../api/boards.js'
import * as ideaReq from '../api/ideas.js'
import * as voteReq from '../api/votings.js'
import * as notifReq from '../api/notifications.js'

const state = reactive(structuredClone(baseState))
setAccessToken(state.auth.accessToken)

const text = {
  anonymous: '\u0430\u043d\u043e\u043d\u0438\u043c\u043d\u043e',
  member: '\u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a',
  requestError: '\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u043f\u0440\u043e\u0441\u0430',
  rejectReason: '\u041f\u0440\u0438\u0447\u0438\u043d\u0430 \u043e\u0442\u043a\u043b\u043e\u043d\u0435\u043d\u0438\u044f',
  voted: '\u0413\u043e\u043b\u043e\u0441 \u0443\u0447\u0442\u0435\u043d',
}

function formatDate(value) {
  if (!value) return ''

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date)
}

function mapBoard(board) {
  return {
    id: board.id,
    title: board.title,
    description: board.description,
    context: board.description || '',
    role: board.role || 'member',
    allowAnonymous: board.anon_ideas ?? true,
    autoApprove: board.moderation === undefined ? false : !board.moderation,
    members: board.members || [],
    createdAt: formatDate(board.created_at),
  }
}

function mapIdea(idea, boardId) {
  return {
    id: idea.id,
    boardId: idea.board_id || boardId,
    title: idea.title,
    description: idea.description,
    status: idea.status,
    isAnonymous: idea.is_anonymous ?? false,
    author: idea.is_anonymous ? text.anonymous : text.member,
    createdAt: formatDate(idea.created_at),
    votesYes: idea.votesYes || 0,
    votesNo: idea.votesNo || 0,
    rejectionReason: idea.rejectionReason || '',
  }
}

function mapMember(member) {
  return {
    id: member.id,
    username: member.username,
    name: member.name || member.username,
    photoUrl: users.fileUrl(member.photo_url),
    role: member.role,
  }
}

function mapNotif(notif) {
  return {
    id: notif.id,
    text: notif.text,
    boardId: notif.board_id,
    createdAt: formatDate(notif.created_at),
  }
}

function mapVoting(voting) {
  return {
    id: voting.id,
    boardId: voting.board_id,
    type: voting.type,
    createdAt: formatDate(voting.created_at),
  }
}

function upsertIdea(idea) {
  const mapped = mapIdea(idea, idea.board_id)
  state.ideas = [mapped, ...state.ideas.filter((item) => item.id !== mapped.id)]
  return mapped
}

function setError(error) {
  state.error = error?.message || text.requestError
}

export function useStore() {
  async function requestLogin(email) {
    state.error = ''
    state.loading = true

    try {
      const data = await auth.login(email)
      return data.exists
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function registerUser(form) {
    state.error = ''
    state.loading = true

    try {
      await auth.register(form)
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function verifyLogin({ email, code }) {
    state.error = ''
    state.loading = true

    try {
      const data = await auth.verify({ email, code })
      state.auth.user = data.user
      state.auth.accessToken = data.access_token
      state.auth.refreshToken = data.refresh_token
      saveTokens({ accessToken: data.access_token, refreshToken: data.refresh_token })
      setAccessToken(data.access_token)
      await loadBoards()
    } catch (error) {
      setError(error)
      throw error
    } finally {
      state.loading = false
    }
  }

  async function checkUsername(username) {
    const data = await users.checkUsername(username)
    return data.available
  }

  async function uploadAvatar(file) {
    const data = await users.uploadAvatar(file)
    return data.photo_url
  }

  function logout() {
    Object.values(state.ws).forEach((ws) => ws?.close())
    clearTokens()
    setAccessToken('')
    state.auth.user = null
    state.auth.accessToken = ''
    state.auth.refreshToken = ''
    state.boards = []
    state.ideas = []
    state.votings = {}
    state.voteResults = {}
    state.notifications = []
    state.ws = {}
  }

  async function loadBoards() {
    const data = await boardReq.getBoards()
    state.boards = data.items.map(mapBoard)
    return state.boards
  }

  async function createBoard(form) {
    const data = await boardReq.createBoard({
      title: form.title,
      description: form.description,
      moderation: form.moderation ?? !form.autoApprove,
      anon_ideas: form.anon_ideas ?? form.allowAnonymous ?? true,
    })

    const board = mapBoard({ ...data, role: 'admin' })
    state.boards.unshift(board)
    return board
  }

  async function loadBoard(boardId) {
    const data = await boardReq.getBoard(boardId)
    const members = await boardReq.getMembers(boardId).catch(() => ({ items: [] }))
    const board = mapBoard(data)
    board.members = members.items.map(mapMember)
    const ideas = (data.ideas || []).map((idea) => mapIdea(idea, board.id))

    state.boards = [board, ...state.boards.filter((item) => item.id !== board.id)]
    state.ideas = [...state.ideas.filter((idea) => idea.boardId !== board.id), ...ideas]

    return board
  }

  async function updateBoard(boardId, form) {
    const data = await boardReq.updateBoard(boardId, {
      title: form.title,
      description: form.description,
      moderation: !form.autoApprove,
      anon_ideas: form.allowAnonymous,
    })

    const old = getBoard(boardId) || {}
    const board = mapBoard({ ...data, role: old.role, members: old.members || [] })
    state.boards = [board, ...state.boards.filter((item) => item.id !== boardId)]
    return board
  }

  async function deleteBoard(boardId) {
    await boardReq.deleteBoard(boardId)
    state.boards = state.boards.filter((board) => board.id !== boardId)
    state.ideas = state.ideas.filter((idea) => idea.boardId !== boardId)
  }

  function getBoard(boardId) {
    return state.boards.find((board) => board.id === boardId)
  }

  async function loadIdeas(boardId) {
    const data = await ideaReq.getBoardIdeas(boardId)
    const ideas = data.items.map((idea) => mapIdea(idea, boardId))

    state.ideas = [...state.ideas.filter((idea) => idea.boardId !== boardId), ...ideas]
    return ideas
  }

  async function loadModerationIdeas(boardId) {
    const data = await ideaReq.getModerationIdeas(boardId)
    const ideas = data.items.map((idea) => mapIdea(idea, boardId))
    const ids = new Set(ideas.map((idea) => idea.id))

    state.ideas = [
      ...state.ideas.filter((idea) => idea.boardId !== boardId || !ids.has(idea.id)),
      ...ideas,
    ]
    return ideas
  }

  function getBoardIdeas(boardId) {
    return state.ideas.filter((idea) => idea.boardId === boardId)
  }

  async function createIdea(boardId, form) {
    const data = await ideaReq.createIdea({
      board_id: boardId,
      title: form.title,
      description: form.description,
      is_anonymous: form.isAnonymous,
    })

    const idea = mapIdea(data, boardId)
    state.ideas = [idea, ...state.ideas.filter((item) => item.id !== idea.id)]
    return idea
  }

  async function deleteIdea(ideaId) {
    await ideaReq.deleteIdea(ideaId)
    state.ideas = state.ideas.filter((idea) => idea.id !== ideaId)
  }

  async function approveIdea(ideaId) {
    const data = await ideaReq.updateIdeaStatus(ideaId, { status: 'approved' })
    return upsertIdea(data)
  }

  async function rejectIdea(ideaId, reason) {
    const data = await ideaReq.updateIdeaStatus(ideaId, {
      status: 'rejected',
      rejection_reason: reason || text.rejectReason,
    })
    const idea = upsertIdea(data)
    idea.rejectionReason = reason || text.rejectReason
    return idea
  }

  async function voteIdea(ideaId) {
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return

    const voting = activeVoting(idea.boardId)
    if (!voting) throw new Error('Нет активного голосования')

    await voteReq.createVote({ voting_id: voting.id, idea_id: ideaId })
    await loadVotingResults(idea.boardId)
  }

  async function addMember(boardId, username) {
    const board = getBoard(boardId)
    if (!board || !username?.trim()) return

    const member = await boardReq.addMember(boardId, { username: username.trim(), role: 'member' })
    board.members = [mapMember(member), ...board.members.filter((item) => item.id !== member.id)]
  }

  async function removeMember(boardId, memberId) {
    const board = getBoard(boardId)
    if (!board) return

    await boardReq.deleteMember(boardId, memberId)
    board.members = board.members.filter((item) => item.id !== memberId)
  }

  async function toggleModerator(boardId, memberId) {
    const member = getBoard(boardId)?.members.find((item) => item.id === memberId)
    if (!member || member.role === 'admin') return

    const role = member.role === 'moderator' ? 'member' : 'moderator'
    const data = await boardReq.updateMemberRole(boardId, memberId, { role })
    Object.assign(member, mapMember(data))
  }

  async function transferAdmin(boardId, memberId) {
    const board = getBoard(boardId)
    if (!board) return

    const next = await boardReq.updateMemberRole(boardId, memberId, { role: 'admin' })
    board.members = board.members.map((member) => (member.id === memberId ? mapMember(next) : member))

    for (const member of board.members.filter((item) => item.id !== memberId && item.role === 'admin')) {
      const data = await boardReq.updateMemberRole(boardId, member.id, { role: 'member' })
      Object.assign(member, mapMember(data))
    }
  }

  function getVoteResults(boardId) {
    return state.voteResults[boardId] || []
  }

  function activeVoting(boardId) {
    return state.votings[boardId]?.[0] || null
  }

  async function loadVotings(boardId) {
    const data = await voteReq.getVotings(boardId)
    state.votings[boardId] = data.items.map(mapVoting)
    await loadVotingResults(boardId)
    return state.votings[boardId]
  }

  async function createVoting(boardId, type = 'yes_no') {
    const voting = mapVoting(await voteReq.createVoting(boardId, { type }))
    state.votings[boardId] = [voting, ...(state.votings[boardId] || []).filter((item) => item.id !== voting.id)]
    await loadVotingResults(boardId)
    return voting
  }

  async function deleteVoting(boardId, votingId) {
    await voteReq.deleteVoting(votingId)
    state.votings[boardId] = (state.votings[boardId] || []).filter((item) => item.id !== votingId)
    state.voteResults[boardId] = []
  }

  async function loadVotingResults(boardId) {
    const voting = activeVoting(boardId)
    if (!voting) {
      state.voteResults[boardId] = []
      return []
    }

    const data = await voteReq.getVotingResults(voting.id)
    state.voteResults[boardId] = data.items.map((item) => {
      const idea = state.ideas.find((row) => row.id === item.idea_id) || {}

      return {
        ...idea,
        id: item.idea_id,
        boardId,
        title: item.title,
        votesCount: item.votes_count,
        approvalPercent: item.approval_percent,
      }
    })
    return state.voteResults[boardId]
  }

  async function loadNotifications() {
    const data = await notifReq.getNotifications()
    state.notifications = data.items.map(mapNotif)
    return state.notifications
  }

  async function deleteNotification(notifId) {
    await notifReq.deleteNotification(notifId)
    state.notifications = state.notifications.filter((item) => item.id !== notifId)
  }

  function connectIdeasWs(boardId) {
    if (!state.auth.accessToken || state.ws[boardId]) return

    const ws = new WebSocket(ideaReq.getIdeasWsUrl(boardId, state.auth.accessToken))
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      if (msg.type === 'idea_created') upsertIdea(msg.idea)
    }
    ws.onclose = () => {
      if (state.ws[boardId] === ws) delete state.ws[boardId]
    }
    state.ws[boardId] = ws
  }

  return {
    state,
    boards: computed(() => state.boards),
    requestLogin,
    registerUser,
    verifyLogin,
    checkUsername,
    uploadAvatar,
    logout,
    loadBoards,
    createBoard,
    loadBoard,
    updateBoard,
    deleteBoard,
    getBoard,
    loadIdeas,
    loadModerationIdeas,
    getBoardIdeas,
    createIdea,
    deleteIdea,
    approveIdea,
    rejectIdea,
    voteIdea,
    addMember,
    removeMember,
    toggleModerator,
    transferAdmin,
    activeVoting,
    loadVotings,
    createVoting,
    deleteVoting,
    getVoteResults,
    loadNotifications,
    deleteNotification,
    connectIdeasWs,
    notifications: computed(() => state.notifications),
  }
}
