export const STATUS_LABELS = {
    not_started: '未受講',
    in_progress: '受講中',
    completed: '完了',
}

export const STATUS_OPTIONS = [
    { value: 'not_started', label: '未受講' },
    { value: 'in_progress', label: '受講中' },
    { value: 'completed', label: '完了' },
]

export function statusLabel(status) {
    return STATUS_LABELS[status] || status
}

export function formatDate(value) {
    if (!value) return '—'
    return value
}

export function formatMinutes(minutes) {
    if (!minutes) return '0分'
    const h = Math.floor(minutes / 60)
    const m = minutes % 60
    if (h === 0) return `${m}分`
    if (m === 0) return `${h}時間`
    return `${h}時間${m}分`
}
