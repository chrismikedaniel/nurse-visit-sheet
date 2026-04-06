-- Nurse Visit Sheet — Supabase Schema
-- Run once in: Supabase Dashboard → SQL Editor → New Query

create table if not exists public.visits (
  id                   uuid primary key default gen_random_uuid(),
  created_at           timestamptz not null default now(),
  center_name          text,
  visit_date           date,
  visit_time           text,
  met_director         boolean default false,
  visited_rooms        boolean default false,
  education_newsletter boolean default false,
  notes                text,
  imm_infant           text,
  imm_toddler          text,
  imm_over18           text,
  imm_mixed            text,
  imm_letters          boolean default false,
  checklist            jsonb default '{}'::jsonb
);

-- Open RLS for anon inserts (tighten for production with auth)
alter table public.visits enable row level security;

create policy "anon insert" on public.visits
  for insert to anon with check (true);

create policy "anon select" on public.visits
  for select to anon using (true);

-- Index for fast lookup by center + date
create index if not exists visits_center_date
  on public.visits (center_name, visit_date desc);
