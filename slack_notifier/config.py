programs = []
events = [
    'PROCESS_STATE_BACKOFF',
    'PROCESS_STATE_FATAL',
    'PROCESS_STATE_EXITED',
    'PROCESS_STATE_STOPPED',
    'PROCESS_STATE_STARTING',
    'PROCESS_STATE_RUNNING']
eventMap = dict(
    PROCESS_STATE_BACKOFF=dict(
        color='danger',
        emoji=':sadpanda:',
    ),
    PROCESS_STATE_FATAL=dict(
        color='danger',
        emoji=':sadpanda:',
    ),
    PROCESS_STATE_EXITED=dict(
        color='danger',
        emoji=':sadpanda:',
    ),
    PROCESS_STATE_STOPPED=dict(
        color='warning',
        emoji=':bambo:',
    ),
    PROCESS_STATE_STARTING=dict(
        color='good',
        emoji=':fuckyeah:',
    ),
    PROCESS_STATE_RUNNING=dict(
        color='good',
        emoji=':fuckyeah:',
    ),
)
