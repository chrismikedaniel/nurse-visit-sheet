# Nurse Visit Sheet — Changelog

## v1.1 — April 2026
- Fixed: Added Anthropic API key (`x-api-key` header) to AI narrative fetch call
- Fixed: API key and Supabase credentials baked into index.html for deployed environment

## v1.0 — April 2026
- Initial release
- AI narrative intake with Claude API + local keyword parser fallback
- 13-section step-by-step wizard (mobile-first)
- Tap-to-cycle checklist: Direct / Evidence / Not Observed / N/A
- Toggle fields for yes/no questions
- Number inputs for immunization file counts per age group
- 2-page print-ready PDF export
- Supabase visit record saving
- PWA support (installable on iOS/Android home screen)
