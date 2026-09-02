import { useEffect, useState } from 'react'
import { CheckCircle2, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ResumeDropzone } from '@/components/ResumeDropzone'
import { getJobs, submitApplication } from '@/lib/api'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const PHONE_PATTERN = /^\+?[0-9 ()-]{7,20}$/
const ALLOWED_RESUME_TYPES = [
  'application/pdf',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]
const MAX_RESUME_SIZE = 5 * 1024 * 1024

function jobLabel(job) {
  const parts = [job.department, job.location].filter(Boolean)
  return parts.length ? `${job.title} — ${parts.join(', ')}` : job.title
}

export default function ApplyPage() {
  const [jobs, setJobs] = useState([])
  const [jobsError, setJobsError] = useState('')

  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [email, setEmail] = useState('')
  const [jobId, setJobId] = useState('')
  const [note, setNote] = useState('')
  const [resume, setResume] = useState(null)

  const [errors, setErrors] = useState({})
  const [submitError, setSubmitError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    getJobs()
      .then(setJobs)
      .catch(() => setJobsError('Could not load open roles. Please refresh the page.'))
  }, [])

  function validate() {
    const next = {}
    if (!name.trim()) next.name = 'Name is required.'
    if (!phone.trim()) next.phone = 'Phone number is required.'
    else if (!PHONE_PATTERN.test(phone.trim())) next.phone = 'Enter a valid phone number.'
    if (!email.trim()) next.email = 'Email is required.'
    else if (!EMAIL_PATTERN.test(email.trim())) next.email = 'Enter a valid email address.'
    if (!jobId) next.job = 'Select a job to apply for.'
    if (!resume) next.resume = 'Attach your resume.'
    else if (!ALLOWED_RESUME_TYPES.includes(resume.type)) next.resume = 'Resume must be a PDF, DOC, or DOCX file.'
    else if (resume.size > MAX_RESUME_SIZE) next.resume = 'Resume must be 5MB or smaller.'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitError('')
    if (!validate()) return

    setSubmitting(true)
    try {
      const formData = new FormData()
      formData.append('name', name.trim())
      formData.append('phone', phone.trim())
      formData.append('email', email.trim())
      formData.append('job_id', jobId)
      formData.append('note', note.trim())
      formData.append('resume', resume)
      await submitApplication(formData)
      setSubmitted(true)
    } catch (err) {
      setSubmitError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (submitted) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background px-4">
        <Card className="w-full max-w-md text-center">
          <CardContent className="flex flex-col items-center gap-3 py-10">
            <CheckCircle2 className="h-12 w-12 text-accent" />
            <h1 className="text-xl font-semibold text-foreground">Application submitted</h1>
            <p className="text-sm text-muted-foreground">
              Thanks for applying — we've received your application and will be in touch if there's a fit.
            </p>
          </CardContent>
        </Card>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen items-start justify-center bg-background px-4 py-10 sm:py-16">
      <Card className="w-full max-w-xl">
        <CardHeader>
          <h1 className="text-2xl font-semibold text-foreground">Apply for a job at enter</h1>
          <p className="text-sm text-muted-foreground">Fill out the form below — it only takes a minute.</p>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-5" onSubmit={handleSubmit} noValidate>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="job">Job</Label>
              <Select value={jobId} onValueChange={setJobId} disabled={!jobs.length && !jobsError}>
                <SelectTrigger id="job" className="w-full" aria-invalid={!!errors.job}>
                  <SelectValue placeholder={jobsError || (jobs.length ? 'Select a job' : 'Loading jobs…')} />
                </SelectTrigger>
                <SelectContent>
                  {jobs.map((job) => (
                    <SelectItem key={job.id} value={job.id}>
                      {jobLabel(job)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.job && <p className="text-sm text-destructive">{errors.job}</p>}
              {jobsError && <p className="text-sm text-destructive">{jobsError}</p>}
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="name">Name</Label>
              <Input id="name" value={name} onChange={(e) => setName(e.target.value)} aria-invalid={!!errors.name} />
              {errors.name && <p className="text-sm text-destructive">{errors.name}</p>}
            </div>

            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="phone">Phone</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  aria-invalid={!!errors.phone}
                />
                {errors.phone && <p className="text-sm text-destructive">{errors.phone}</p>}
              </div>
              <div className="flex flex-col gap-1.5">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  aria-invalid={!!errors.email}
                />
                {errors.email && <p className="text-sm text-destructive">{errors.email}</p>}
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <Label>Resume</Label>
              <ResumeDropzone file={resume} onFileSelect={setResume} error={errors.resume} />
              {errors.resume && <p className="text-sm text-destructive">{errors.resume}</p>}
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="note">A brief note (optional)</Label>
              <Textarea id="note" rows={4} value={note} onChange={(e) => setNote(e.target.value)} />
            </div>

            {submitError && (
              <p className="rounded-md bg-stage-reject-bg px-3 py-2 text-sm text-stage-reject-fg">{submitError}</p>
            )}

            <Button type="submit" size="lg" disabled={submitting} className="w-full">
              {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
              {submitting ? 'Submitting…' : 'Submit application'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  )
}
