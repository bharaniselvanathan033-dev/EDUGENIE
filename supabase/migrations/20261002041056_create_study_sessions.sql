/*
# Create study_sessions table for EduGenie AI

1. Purpose
   Stores a user's study sessions so they can revisit past explanations,
   quizzes, summaries, and learning paths. This is a single-tenant app
   (no sign-in screen) so all data is shared/public with anon access.

2. New Tables
   - `study_sessions`
     - `id` (uuid, primary key)
     - `mode` (text: explain | quiz | summary | learning_path)
     - `level` (text: beginner | intermediate | advanced)
     - `topic` (text, the user's input topic/notes)
     - `result` (text, the generated output stored as JSON string)
     - `created_at` (timestamptz, defaults to now())

3. Security
   - RLS enabled on `study_sessions`.
   - Anon + authenticated CRUD allowed because the app has no sign-in
     and the data is intentionally shared/public.
*/

CREATE TABLE IF NOT EXISTS study_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  mode text NOT NULL CHECK (mode IN ('explain', 'quiz', 'summary', 'learning_path')),
  level text NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
  topic text NOT NULL,
  result text NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE study_sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_select_sessions" ON study_sessions;
CREATE POLICY "anon_select_sessions" ON study_sessions FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_sessions" ON study_sessions;
CREATE POLICY "anon_insert_sessions" ON study_sessions FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_update_sessions" ON study_sessions;
CREATE POLICY "anon_update_sessions" ON study_sessions FOR UPDATE
  TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_sessions" ON study_sessions;
CREATE POLICY "anon_delete_sessions" ON study_sessions FOR DELETE
  TO anon, authenticated USING (true);
