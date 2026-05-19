import { computed, reactive, watch } from 'vue'
import { defaultState } from './defaultState.js'
import { loadState, saveState, resetState as clearStorage } from '../utils/storage.js'

const state = reactive(loadState(defaultState))

watch(
  state,
  () => saveState(state),
  { deep: true }
)

function nextId(items) {
  return items.length ? Math.max(...items.map((item) => item.id)) + 1 : 1
}

export function useAppStore() {
  function login({ email }) {
    state.auth.email = email
  }

  function resetAll() {
    clearStorage()
    Object.assign(state, loadState(defaultState))
  }

  function createBoard(payload) {
    const board = {
      id: nextId(state.boards),
      title: payload.title || 'Новая доска',
      description: payload.description || 'Описание доски',
      context: payload.context || payload.description || '',
      role: 'Админ',
      allowAnonymous: true,
      autoApprove: false,
      members: [{ id: Date.now(), name: state.auth.userName || 'чел 1', role: 'Админ' }],
    }
    state.boards.unshift(board)
    return board
  }

  function updateBoard(boardId, payload) {
    const board = getBoard(boardId)
    if (!board) return
    Object.assign(board, payload)
  }

  function deleteBoard(boardId) {
    state.boards = state.boards.filter((board) => board.id !== boardId)
    state.ideas = state.ideas.filter((idea) => idea.boardId !== boardId)
  }

  function getBoard(boardId) {
    return state.boards.find((board) => board.id === Number(boardId))
  }

  function getBoardIdeas(boardId) {
    return state.ideas.filter((idea) => idea.boardId === Number(boardId))
  }

  function createIdea(boardId, payload) {
    const board = getBoard(boardId)
    const idea = {
      id: nextId(state.ideas),
      boardId: Number(boardId),
      title: payload.title || 'Новая идея',
      description: payload.description || 'Описание идеи',
      status: board?.autoApprove ? 'approved' : 'pending',
      isAnonymous: board?.allowAnonymous ? !!payload.isAnonymous : false,
      author: state.auth.userName || 'чел 1',
      createdAt: 'сегодня',
      votesYes: 0,
      votesNo: 0,
      rejectionReason: '',
    }
    state.ideas.unshift(idea)
    return idea
  }

  function deleteIdea(ideaId) {
    state.ideas = state.ideas.filter((idea) => idea.id !== ideaId)
  }

  function approveIdea(ideaId) {
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    idea.status = 'approved'
    idea.rejectionReason = ''
  }

  function rejectIdea(ideaId, reason) {
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    idea.status = 'rejected'
    idea.rejectionReason = reason || 'Причина отклонения'
  }

  function voteIdea(ideaId, type) {
    const idea = state.ideas.find((item) => item.id === ideaId)
    if (!idea) return
    if (type === 'yes') idea.votesYes += 1
    if (type === 'no') idea.votesNo += 1
  }

  function addMember(boardId, name) {
    const board = getBoard(boardId)
    if (!board || !name?.trim()) return
    board.members.push({ id: Date.now(), name: name.trim(), role: 'Участник' })
  }

  function removeMember(boardId, memberId) {
    const board = getBoard(boardId)
    if (!board) return
    const member = board.members.find((item) => item.id === memberId)
    if (member?.role === 'Админ') return
    board.members = board.members.filter((item) => item.id !== memberId)
  }

  function toggleModerator(boardId, memberId) {
    const board = getBoard(boardId)
    const member = board?.members.find((item) => item.id === memberId)
    if (!member || member.role === 'Админ') return
    member.role = member.role === 'Модератор' ? 'Участник' : 'Модератор'
  }

  function transferAdmin(boardId, memberId) {
    const board = getBoard(boardId)
    if (!board) return
    board.members = board.members.map((member) => ({
      ...member,
      role: member.id === memberId ? 'Админ' : member.role === 'Админ' ? 'Участник' : member.role,
    }))
    board.role = memberId ? 'Участник' : board.role
  }

  function getVoteResults(boardId) {
    return getBoardIdeas(boardId)
      .filter((idea) => idea.status === 'approved')
      .map((idea) => {
        const total = idea.votesYes + idea.votesNo
        return { ...idea, approvalPercent: total ? Math.round((idea.votesYes / total) * 100) : 0 }
      })
  }

  return {
    state,
    boards: computed(() => state.boards),
    login,
    resetAll,
    createBoard,
    updateBoard,
    deleteBoard,
    getBoard,
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
    getVoteResults,
  }
}
