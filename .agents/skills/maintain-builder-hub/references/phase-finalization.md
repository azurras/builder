# Phase Finalization

Use this once at the end of an authorized artifact-writing phase:

1. Finish the intended artifacts, linking primary evidence and updating related status. Keep existing content unless intentional replacement is authorized.
2. Run `maintain-builder-hub` **refresh** to regenerate indexes and validate. Fix errors and review resulting diffs. A failed validation blocks publication; do not hide it by editing generated evidence or downgrading status inaccurately.
3. Invoke `commit-push-builder-main`, inspect Git state and outgoing commits, and dry-run an explicit list of intended files. Commit/push that same reviewed selection. Preserve unrelated staged/dirty work. A failed push leaves the checkpoint incomplete; retain the commit and retry publication through the push-only mode after diagnosis.
4. Confirm publication before starting the next delivery phase. Implementation plan, applicable runtime report, and continuity remain separate checkpoints. Do not combine those phases into one delayed commit.

A single phase may append project memory and update indexes with its primary plan or report. Maintenance, review, registration, and coordination substeps do not each create session memory. Save continuity at substantive completion or an authorized handoff. Record proposed external closure before acting; append and publish the verified actual result afterward. Check-only/review-only requests do not enter this finalizer unless the user also requests persistence.
