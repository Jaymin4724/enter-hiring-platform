import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL

async function parseErrorDetail(res) {
  try {
    const body = await res.json()
    if (Array.isArray(body.detail)) {
      return body.detail.map((d) => d.msg).join(', ')
    }
    return body.detail || 'Something went wrong. Please try again.'
  } catch {
    return 'Something went wrong. Please try again.'
  }
}

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, { method = 'GET', json, body, auth = false } = {}) {
  const headers = { ...(auth ? authHeaders() : {}) }
  if (json !== undefined) headers['Content-Type'] = 'application/json'

  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: json !== undefined ? JSON.stringify(json) : body,
  })

  if (!res.ok) {
    const error = new Error(await parseErrorDetail(res))
    error.status = res.status
    throw error
  }
  if (res.status === 204) return null
  return res.json()
}

export async function login(email, password) {
  return request('/auth/login', { method: 'POST', json: { email, password } })
}

export async function getJobs() {
  return request('/jobs')
}

export async function createJob(data) {
  return request('/jobs', { method: 'POST', json: data, auth: true })
}

export async function updateJob(id, data) {
  return request(`/jobs/${id}`, { method: 'PUT', json: data, auth: true })
}

export async function deleteJob(id) {
  return request(`/jobs/${id}`, { method: 'DELETE', auth: true })
}

export async function submitApplication(formData) {
  return request('/applications', { method: 'POST', body: formData })
}
