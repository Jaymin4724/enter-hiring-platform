import { useEffect, useState } from 'react'
import { Loader2, Pencil, Plus, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter, SheetDescription } from '@/components/ui/sheet'
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogAction,
  AlertDialogCancel,
} from '@/components/ui/alert-dialog'
import { createJob, deleteJob, getJobs, updateJob } from '@/lib/api'

const EMPTY_FORM = { title: '', department: '', location: '', description: '' }

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export default function JobsPage() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [sheetOpen, setSheetOpen] = useState(false)
  const [editingJob, setEditingJob] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [formError, setFormError] = useState('')
  const [saving, setSaving] = useState(false)

  const [deleteTarget, setDeleteTarget] = useState(null)
  const [deleting, setDeleting] = useState(false)

  async function fetchJobs() {
    setLoading(true)
    setError('')
    try {
      const data = await getJobs()
      setJobs(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [])

  function openCreate() {
    setEditingJob(null)
    setForm(EMPTY_FORM)
    setFormError('')
    setSheetOpen(true)
  }

  function openEdit(job) {
    setEditingJob(job)
    setForm({
      title: job.title,
      department: job.department ?? '',
      location: job.location ?? '',
      description: job.description ?? '',
    })
    setFormError('')
    setSheetOpen(true)
  }

  async function handleSave(e) {
    e.preventDefault()
    if (!form.title.trim()) {
      setFormError('Title is required.')
      return
    }
    if (form.title.trim().length > 200) {
      setFormError('Title must be 200 characters or fewer.')
      return
    }
    setFormError('')
    setSaving(true)
    try {
      const payload = {
        title: form.title.trim(),
        department: form.department.trim() || null,
        location: form.location.trim() || null,
        description: form.description.trim() || null,
      }
      if (editingJob) {
        await updateJob(editingJob.id, payload)
      } else {
        await createJob(payload)
      }
      setSheetOpen(false)
      await fetchJobs()
    } catch (err) {
      setFormError(err.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleConfirmDelete() {
    if (!deleteTarget) return
    setDeleting(true)
    try {
      await deleteJob(deleteTarget.id)
      setDeleteTarget(null)
      await fetchJobs()
    } catch (err) {
      setError(err.message)
      setDeleteTarget(null)
    } finally {
      setDeleting(false)
    }
  }

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-semibold text-foreground">Jobs</h1>
        <Button type="button" className="h-10 gap-1.5" onClick={openCreate}>
          <Plus className="h-4 w-4" />
          Add job
        </Button>
      </div>

      {error && <p className="rounded-md bg-stage-reject-bg px-3 py-2 text-sm text-stage-reject-fg">{error}</p>}

      {loading ? (
        <div className="flex items-center justify-center gap-2 rounded-lg border border-border bg-card py-12 text-sm text-muted-foreground">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading jobs…
        </div>
      ) : (
        <div className="rounded-lg border border-border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Created</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobs.map((job) => (
                <TableRow key={job.id}>
                  <TableCell className="font-medium text-foreground">{job.title}</TableCell>
                  <TableCell className="text-muted-foreground">{job.department || '—'}</TableCell>
                  <TableCell className="text-muted-foreground">{job.location || '—'}</TableCell>
                  <TableCell className="text-muted-foreground">{formatDate(job.created_at)}</TableCell>
                  <TableCell>
                    <div className="flex justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-10 w-10"
                        aria-label={`Edit ${job.title}`}
                        onClick={() => openEdit(job)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        className="h-10 w-10 text-destructive hover:text-destructive"
                        aria-label={`Delete ${job.title}`}
                        onClick={() => setDeleteTarget(job)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
              {jobs.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="py-8 text-center text-muted-foreground">
                    No jobs yet. Add one to get started.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}

      <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>{editingJob ? 'Edit job' : 'Add job'}</SheetTitle>
            <SheetDescription>
              {editingJob ? 'Update this role — changes apply immediately.' : 'This role appears in the candidate dropdown right away.'}
            </SheetDescription>
          </SheetHeader>
          <form className="flex flex-1 flex-col gap-4 overflow-y-auto px-4" onSubmit={handleSave}>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="job-title">Title</Label>
              <Input
                id="job-title"
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                aria-invalid={!!formError}
                maxLength={200}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="job-department">Department</Label>
              <Input
                id="job-department"
                value={form.department}
                onChange={(e) => setForm((f) => ({ ...f, department: e.target.value }))}
                maxLength={120}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="job-location">Location</Label>
              <Input
                id="job-location"
                value={form.location}
                onChange={(e) => setForm((f) => ({ ...f, location: e.target.value }))}
                maxLength={120}
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="job-description">Description</Label>
              <Textarea
                id="job-description"
                rows={4}
                value={form.description}
                onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
                maxLength={5000}
              />
            </div>
            {formError && <p className="text-sm text-destructive">{formError}</p>}
            <SheetFooter className="mt-auto px-0">
              <Button type="submit" className="h-10 w-full" disabled={saving}>
                {saving && <Loader2 className="h-4 w-4 animate-spin" />}
                {saving ? 'Saving…' : 'Save'}
              </Button>
            </SheetFooter>
          </form>
        </SheetContent>
      </Sheet>

      <AlertDialog open={!!deleteTarget} onOpenChange={(open) => !open && setDeleteTarget(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this job?</AlertDialogTitle>
            <AlertDialogDescription>
              {deleteTarget && `"${deleteTarget.title}" will be permanently removed. This can't be undone.`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={deleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              disabled={deleting}
              onClick={(e) => {
                e.preventDefault()
                handleConfirmDelete()
              }}
            >
              {deleting ? 'Deleting…' : 'Delete'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
