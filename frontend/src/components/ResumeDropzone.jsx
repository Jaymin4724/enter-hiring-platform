import { useRef, useState } from 'react'
import { FileText, UploadCloud, X } from 'lucide-react'
import { cn } from '@/lib/utils'

function formatSize(bytes) {
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function ResumeDropzone({ file, onFileSelect, error }) {
  const inputRef = useRef(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleDrop(e) {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files?.[0]
    if (dropped) onFileSelect(dropped)
  }

  if (file) {
    return (
      <div className="flex items-center justify-between rounded-lg border border-border bg-muted px-4 py-3">
        <div className="flex min-w-0 items-center gap-3">
          <FileText className="h-5 w-5 shrink-0 text-primary" />
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-foreground">{file.name}</p>
            <p className="text-xs text-muted-foreground">{formatSize(file.size)}</p>
          </div>
        </div>
        <button
          type="button"
          onClick={() => onFileSelect(null)}
          className="shrink-0 rounded-md p-1.5 text-muted-foreground hover:bg-background hover:text-foreground"
          aria-label="Remove resume"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    )
  }

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={cn(
        'flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed px-4 py-8 text-center transition-colors',
        isDragging ? 'border-primary bg-secondary' : 'border-border bg-muted/50 hover:bg-muted',
        error && 'border-destructive'
      )}
    >
      <UploadCloud className="h-8 w-8 text-muted-foreground" />
      <p className="text-sm text-foreground">
        <span className="font-medium text-primary">Click to upload</span> or drag and drop
      </p>
      <p className="text-xs text-muted-foreground">PDF, DOC, or DOCX — up to 5MB</p>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        className="hidden"
        onChange={(e) => onFileSelect(e.target.files?.[0] ?? null)}
      />
    </div>
  )
}
