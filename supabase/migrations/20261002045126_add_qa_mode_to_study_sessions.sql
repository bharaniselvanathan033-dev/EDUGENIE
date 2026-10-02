/*
# Update study_sessions to support Q&A mode

1. Changes
   - The `mode` column now also accepts 'qa' as a valid value.
   - This allows saving AI Question & Answer sessions alongside
     the existing explain/quiz/summary/learning_path sessions.

2. Security
   - No policy changes. Existing anon + authenticated CRUD policies
     already cover the new mode value.
*/

ALTER TABLE study_sessions
  DROP CONSTRAINT IF EXISTS study_sessions_mode_check;

ALTER TABLE study_sessions
  ADD CONSTRAINT study_sessions_mode_check
  CHECK (mode IN ('qa', 'explain', 'quiz', 'summary', 'learning_path'));
