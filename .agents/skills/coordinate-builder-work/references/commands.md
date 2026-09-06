# Coordination Commands

Pass the complete reviewed Markdown body on stdin. All commands accept `--root . --title 'Title'`, optional `--date YYYY-MM-DD`, and intentional full replacement with `--overwrite` after reading the existing file.

| Mode | Command |
| --- | --- |
| Start | `python .agents/skills/start-hub-work/scripts/start_hub_work.py` |
| Dispatch | `python .agents/skills/dispatch-spoke-task/scripts/dispatch_spoke_task.py` |
| Update | `python .agents/skills/ingest-spoke-update/scripts/ingest_spoke_update.py` |
| Close | `python .agents/skills/close-hub-work/scripts/close_hub_work.py` |

The legacy command locations remain supported. They save dated Markdown and refuse accidental overwrites; they do not launch agents, change source repositories, post updates, or commit. Review the intended artifact before phase finalization.
