# Weekly update instructions (for Claude)

This repo is Majid Khan's public PhD outreach dashboard, served by GitHub Pages from `main`.
`index.html` renders everything from `data.js`. A scheduled task runs once a week and follows
these steps. Do not change `index.html` during a weekly run unless something is broken.

## Hard rules

1. **Never send, reply to, draft, label, archive or delete any email.** Gmail is read-only here.
2. **Privacy — the site is public.** Store only university, country, dates, categories and short
   generic notes. Never put professor names, email addresses, quoted email text, CGPA details,
   or document contents into `data.js`.
3. **Never mention NUST MISIS** (or any current enrolment) anywhere in the repo.
4. Don't invent anything. If a reply is ambiguous, use `cat: "unclear"`. If a deadline isn't
   confirmed on an official page, use `status: "expected"`.
5. Run `python3 scripts/validate_data.py` before committing. If it fails, fix the data; never commit invalid data.

## Weekly procedure

1. Read `data.js`. Note `updatedISO` (the last sync date, YYYY-MM-DD) — call it LAST.
2. **New replies.** Search Gmail for messages from others since LAST, e.g.
   `-from:me after:LAST (subject:PhD OR subject:doctoral OR subject:inquiry OR subject:enquiry OR subject:application OR subject:position)`.
   Also check threads where a professor replied to a follow-up. Read each thread (use get_thread,
   because search previews omit newer messages). For each *professor or admissions* reply, add one
   entry to `replies` (newest first):
   `{"uni","country","cat","date","reason"?}`
   - `positive`: interest, support letter, asks for documents, invites a call, offers hosting.
   - `apply`: tells him to apply formally / fill a form / use a program route.
   - `negative`: no position, no funding, lab full, not a fit, retired. Add `reason`, one of:
     `No open position`, `No funding`, `Lab at capacity`, `Not a research fit`,
     `Retired / role change`, `No intl. students`.
   - `auto`: out-of-office or automatic acknowledgement.
   - `unclear`: anything else (e.g. generic office forwarding).
   Skip duplicates already in `replies` (same uni + date + cat).
3. **Sent count.** Use the Gmail `resultCountEstimate` for
   `in:sent after:LAST subject:(PhD OR doctoral OR prospective) -subject:Re` and add it to `sent`
   (keep `sentApprox: true`). Append `{"date": TODAY, "total": sent}` to `sentLog`.
   Count new bounces (`from:mailer-daemon after:LAST`) and add to `bounced`.
4. **Leads.** Update `leads` (`stage`: waiting | apply | applied | check | later; `heat`: hot | warm):
   - New positive/apply replies become leads.
   - If a lead's professor declined, remove the lead.
   - If Majid replied/applied, move the stage forward and update `next`.
   - Keep `note` and `next` short and generic (no names).
5. **Actions** (`type`: followup | apply | portal | form | reply; `due`: YYYY-MM-DD):
   - Remove actions that are done (e.g. follow-up already sent, application confirmation received).
   - Add `reply` actions for professor messages awaiting Majid's answer (due: 2 days after receipt).
   - Add `followup` actions for first-contact emails 6+ days old with no reply and no previous
     follow-up, grouped by batch (e.g. "Follow up on 12 Finland emails from Nov 14"). Never suggest
     a third email to the same professor.
   - Keep the list focused: at most ~12 items, soonest first.
6. **Deadlines.** Drop nothing; past deadlines grey out automatically. Add new ones mentioned in
   emails (portal confirmations, program announcements). Upgrade `expected` → `confirmed` only with an
   official source.
7. Set `updated` (e.g. "30 Nov 2026") and `updatedISO` (TODAY). Prepend one line to `log`
   summarising the week: new replies by type, new leads, notable changes.
8. Validate, then commit and push to `main`:
   `git add data.js && git commit -m "Weekly sync YYYY-MM-DD" && git push origin main`
9. Finish with a short summary for Majid: new positive replies, actions due this week, and anything
   that needs his decision.

## Data schema (data.js)

```
window.DATA = {
  replies:   [{uni, country, cat, date, reason?}],
  leads:     [{uni, country, note, next, stage, heat, since}],
  actions:   [{type, text, due}],
  deadlines: [{name, date, status, note}],
  sent, sentApprox, bounced, sentLog: [{date, total}],
  updated, updatedISO, log: [string]
};
```
