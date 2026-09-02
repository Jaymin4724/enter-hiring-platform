import { useEffect, useState } from 'react'
import { Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { getApplications, getJobs, getResumeUrl, updateApplicationStage } from '@/lib/api'
import { STAGES, stageBadgeClass } from '@/lib/stages'
import { cn } from '@/lib/utils'

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export default function CandidatesPage() {
  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [jobFilter, setJobFilter] = useState('all')
  const [stageFilter, setStageFilter] = useState('all')

  const [stageUpdating, setStageUpdating] = useState(null)
  const [resumeLoading, setResumeLoading] = useState(null)

  async function fetchApplications(jobId, stage) {
    setLoading(true)
    setError('')
    try {
      const data = await getApplications({
        jobId: jobId !== 'all' ? jobId : undefined,
        stage: stage !== 'all' ? stage : undefined,
      })
      setApplications(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    getJobs()
      .then(setJobs)
      .catch(() => {})
    fetchApplications('all', 'all')
  }, [])

  function handleJobFilterChange(value) {
    setJobFilter(value)
    fetchApplications(value, stageFilter)
  }

  function handleStageFilterChange(value) {
    setStageFilter(value)
    fetchApplications(jobFilter, value)
  }

  function jobTitle(jobId) {
    return jobs.find((job) => job.id === jobId)?.title || '—'
  }

  async function handleStageChange(application, newStage) {
    setStageUpdating(application.id)
    setError('')
    try {
      const updated = await updateApplicationStage(application.id, newStage)
      setApplications((prev) => prev.map((a) => (a.id === application.id ? updated : a)))
    } catch (err) {
      setError(err.message)
    } finally {
      setStageUpdating(null)
    }
  }

  async function handleViewResume(application) {
    setResumeLoading(application.id)
    setError('')
    try {
      const { url } = await getResumeUrl(application.id)
      window.open(url, '_blank', 'noopener,noreferrer')
    } catch (err) {
      setError(err.message)
    } finally {
      setResumeLoading(null)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-semibold text-foreground">Candidates</h1>

      <div className="flex flex-wrap gap-3">
        <Select value={jobFilter} onValueChange={handleJobFilterChange}>
          <SelectTrigger className="w-full sm:w-56" aria-label="Filter by job">
            <SelectValue placeholder="All jobs" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All jobs</SelectItem>
            {jobs.map((job) => (
              <SelectItem key={job.id} value={job.id}>
                {job.title}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={stageFilter} onValueChange={handleStageFilterChange}>
          <SelectTrigger className="w-full sm:w-56" aria-label="Filter by stage">
            <SelectValue placeholder="All stages" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All stages</SelectItem>
            {STAGES.map((stage) => (
              <SelectItem key={stage} value={stage}>
                {stage}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {error && <p className="rounded-md bg-stage-reject-bg px-3 py-2 text-sm text-stage-reject-fg">{error}</p>}

      {loading ? (
        <div className="flex items-center justify-center gap-2 rounded-lg border border-border bg-card py-12 text-sm text-muted-foreground">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading candidates…
        </div>
      ) : (
        <div className="rounded-lg border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Phone</TableHead>
                <TableHead>Job</TableHead>
                <TableHead>Stage</TableHead>
                <TableHead>Applied</TableHead>
                <TableHead className="text-right">Resume</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {applications.map((application) => (
                <TableRow key={application.id}>
                  <TableCell className="font-medium text-foreground">{application.name}</TableCell>
                  <TableCell className="text-muted-foreground">{application.email}</TableCell>
                  <TableCell className="text-muted-foreground">{application.phone}</TableCell>
                  <TableCell className="text-muted-foreground">{jobTitle(application.job_id)}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Select
                        value={application.stage}
                        onValueChange={(value) => handleStageChange(application, value)}
                        disabled={stageUpdating === application.id}
                      >
                        <SelectTrigger
                          size="sm"
                          className={cn(
                            'h-7 w-auto min-w-[7.5rem] rounded-full border-none px-2.5 text-xs font-medium shadow-none',
                            stageBadgeClass(application.stage)
                          )}
                          aria-label={`Change stage for ${application.name}`}
                        >
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {STAGES.map((stage) => (
                            <SelectItem key={stage} value={stage}>
                              {stage}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      {stageUpdating === application.id && (
                        <Loader2 className="h-3.5 w-3.5 animate-spin text-muted-foreground" />
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{formatDate(application.created_at)}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="h-10"
                      onClick={() => handleViewResume(application)}
                      disabled={resumeLoading === application.id}
                    >
                      {resumeLoading === application.id ? <Loader2 className="h-4 w-4 animate-spin" /> : 'View resume'}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {applications.length === 0 && (
                <TableRow>
                  <TableCell colSpan={7} className="py-8 text-center text-muted-foreground">
                    {jobFilter !== 'all' || stageFilter !== 'all'
                      ? 'No candidates match these filters.'
                      : 'No applications yet.'}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
