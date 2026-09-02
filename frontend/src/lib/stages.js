export const STAGES = ['Applied', 'Reject', 'R1', 'R1 Reject', 'R2', 'R2 Reject', 'R3', 'R3 Reject', 'Approved']

export function stageBadgeClass(stage) {
  if (stage.includes('Reject')) return 'bg-stage-reject-bg text-stage-reject-fg'
  switch (stage) {
    case 'Applied':
      return 'bg-stage-applied-bg text-stage-applied-fg'
    case 'R1':
      return 'bg-stage-r1-bg text-stage-r1-fg'
    case 'R2':
      return 'bg-stage-r2-bg text-stage-r2-fg'
    case 'R3':
      return 'bg-stage-r3-bg text-stage-r3-fg'
    case 'Approved':
      return 'bg-stage-approved-bg text-stage-approved-fg'
    default:
      return 'bg-stage-applied-bg text-stage-applied-fg'
  }
}
