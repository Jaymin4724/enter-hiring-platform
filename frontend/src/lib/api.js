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

export async function getJobs() {
  const res = await fetch(`${API_URL}/jobs`)
  if (!res.ok) throw new Error(await parseErrorDetail(res))
  return res.json()
}

export async function submitApplication(formData) {
  const res = await fetch(`${API_URL}/applications`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    const error = new Error(await parseErrorDetail(res))
    error.status = res.status
    throw error
  }
  return res.json()
}
