# Heartbeat

> Unified status page and healthcheck monitoring for all deployed projects

**Status:** 💡 idea
**GitHub:** -
**Tech Stack:** Next.js, Convex/Supabase, Upstash QStash, Vercel

## Overview

A central status dashboard that monitors all your deployed projects with:
- One dashboard at `status.yourdomain.com`
- Subdomain per project: `scry.status.yourdomain.com`, `sploot.status.yourdomain.com`
- Simple healthcheck endpoints for each service
- Real-time up/down status
- Historical uptime data
- Alerts when things break
- Public status pages (shareable)

**Primary use case:** Monitor your own projects (scry, sploot, vanity, chrondle, hmm, etc.)

**Secondary opportunity:** Product for solo devs tired of StatusPage.io pricing ($29+/month)

## Personal Use Case

### Current Pain
- No visibility into which projects are actually running
- Manual checks to verify deployments
- Don't know when something breaks until users report it
- No historical uptime data

### Desired State
- Dashboard shows all projects at a glance
- Email/SMS alerts when service goes down
- Public status page to share with users
- Historical data to track reliability

### Projects to Monitor
- scry (web app)
- sploot (web app)
- vanity (personal site)
- chrondle (web game)
- hmm (web app)
- misty-step (web app)
- volume (mobile backend?)
- whetstone (mobile backend?)
- Any future deployments

## Core Features

### MVP (Personal Use)
1. **Dashboard**
   - List all monitored projects
   - Current status (🟢 up, 🔴 down, 🟡 degraded)
   - Response time graphs
   - Uptime percentage (24h, 7d, 30d)

2. **Healthchecks**
   - HTTP endpoint checks (`GET /health`)
   - Expected status code (default 200)
   - Response time tracking
   - Configurable interval (1min, 5min, 15min)
   - Timeout threshold

3. **Alerts**
   - Email on downtime
   - SMS for critical services (optional)
   - Slack/Discord webhook (optional)
   - Alert grouping (don't spam on flapping)

4. **Configuration**
   - Add/remove projects via UI
   - Set check intervals per project
   - Configure alert channels
   - Define what "down" means (# failed checks)

### V2 (Product Features)
5. **Public Status Pages**
   - Shareable URLs: `scry.status.heartbeat.dev`
   - Custom domains: `status.scry.com`
   - Incident posting
   - Subscribe to updates
   - Historical incidents

6. **Advanced Checks**
   - TCP port checks
   - DNS resolution checks
   - Database connection checks
   - Custom webhook checks
   - SSL certificate expiry monitoring

7. **Integrations**
   - GitHub Actions (deploy = auto-add check)
   - Vercel deployment hooks
   - Railway deployment hooks
   - PagerDuty escalation

8. **Team Features**
   - Multi-user access
   - On-call rotation
   - Incident management
   - Postmortem templates

## Architecture

### Infrastructure
```
User → Vercel (Next.js) → Convex/Supabase (data)
                       ↓
              Upstash QStash (cron checks)
                       ↓
              Your Projects (healthcheck endpoints)
                       ↓
              Resend/Twilio (alerts)
```

### Data Model

**Projects**
```typescript
{
  id: string
  name: string
  url: string
  healthcheckEndpoint: string  // e.g., /health, /api/ping
  checkInterval: number        // seconds
  expectedStatus: number       // 200, 204, etc.
  timeout: number              // milliseconds
  alertChannels: string[]      // email, sms, slack
  createdAt: timestamp
  updatedAt: timestamp
}
```

**Checks**
```typescript
{
  id: string
  projectId: string
  status: 'up' | 'down' | 'degraded'
  responseTime: number         // milliseconds
  statusCode: number | null
  error: string | null
  checkedAt: timestamp
}
```

**Incidents**
```typescript
{
  id: string
  projectId: string
  title: string
  description: string
  status: 'investigating' | 'identified' | 'monitoring' | 'resolved'
  startedAt: timestamp
  resolvedAt: timestamp | null
  updates: IncidentUpdate[]
}
```

### Healthcheck Implementation

**In your apps (e.g., scry, sploot):**
```typescript
// app/api/health/route.ts
export async function GET() {
  try {
    // Check database connection
    await db.ping()

    // Check critical services
    // ...

    return Response.json({
      status: 'ok',
      timestamp: Date.now(),
      version: process.env.VERCEL_GIT_COMMIT_SHA
    })
  } catch (error) {
    return Response.json(
      { status: 'error', error: error.message },
      { status: 503 }
    )
  }
}
```

**In heartbeat (checker):**
```typescript
// Upstash QStash handler
export async function checkProject(project: Project) {
  const startTime = Date.now()

  try {
    const response = await fetch(
      `${project.url}${project.healthcheckEndpoint}`,
      {
        signal: AbortSignal.timeout(project.timeout),
        headers: { 'User-Agent': 'Heartbeat/1.0' }
      }
    )

    const responseTime = Date.now() - startTime
    const isUp = response.status === project.expectedStatus

    await recordCheck({
      projectId: project.id,
      status: isUp ? 'up' : 'down',
      responseTime,
      statusCode: response.status,
      checkedAt: new Date()
    })

    if (!isUp) {
      await triggerAlert(project, response.status)
    }
  } catch (error) {
    await recordCheck({
      projectId: project.id,
      status: 'down',
      responseTime: Date.now() - startTime,
      statusCode: null,
      error: error.message,
      checkedAt: new Date()
    })

    await triggerAlert(project, error)
  }
}
```

## Tech Stack

### Frontend
- **Next.js 14** - App router, server components
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **Recharts** - Uptime graphs
- **TanStack Query** - Data fetching

### Backend
- **Convex** (preferred) or **Supabase**
  - Real-time subscriptions
  - Serverless functions
  - Built-in auth

### Monitoring
- **Upstash QStash** - Cron job scheduler
  - HTTP-based, no infrastructure
  - Retry logic built-in
  - $10/month for 500k requests

### Alerts
- **Resend** - Email alerts (100/day free)
- **Twilio** - SMS alerts (pay-as-you-go)
- **Webhooks** - Slack/Discord (free)

### Hosting
- **Vercel** - Frontend + API routes
- **Custom domain** - status.yourdomain.com

## Implementation Roadmap

### Phase 1: MVP (Personal Use)
**Goal:** Monitor your own projects

1. **Week 1: Core Infrastructure**
   - [ ] Next.js app setup
   - [ ] Convex schema + functions
   - [ ] Dashboard UI (list projects)
   - [ ] Add/edit project form

2. **Week 2: Healthchecks**
   - [ ] Upstash QStash integration
   - [ ] HTTP check implementation
   - [ ] Store check results
   - [ ] Display current status

3. **Week 3: Alerts & Polish**
   - [ ] Email alerts via Resend
   - [ ] Alert grouping logic
   - [ ] Response time graphs
   - [ ] Uptime calculations
   - [ ] Deploy to Vercel

4. **Week 4: Dogfooding**
   - [ ] Add all your projects
   - [ ] Create `/health` endpoints in each app
   - [ ] Test alert flow
   - [ ] Fix bugs & UX issues

### Phase 2: Public Status Pages
**Goal:** Shareable status pages for users

5. **Week 5: Public Pages**
   - [ ] Public status page UI
   - [ ] Subdomain routing
   - [ ] Subscribe to updates
   - [ ] Custom branding per project

6. **Week 6: Incident Management**
   - [ ] Create/update incidents
   - [ ] Incident timeline
   - [ ] Notification to subscribers
   - [ ] Postmortem templates

### Phase 3: Product Launch (Optional)
**Goal:** Offer as paid product to solo devs

7. **Week 7: Multi-tenancy**
   - [ ] User authentication
   - [ ] Workspace/team concept
   - [ ] Usage limits per tier
   - [ ] Billing integration (Stripe)

8. **Week 8: Marketing**
   - [ ] Landing page
   - [ ] Documentation
   - [ ] Pricing page ($5-15/month)
   - [ ] Launch on Twitter/HN

## Pricing Model (Product Version)

### Solo ($5/month)
- 5 monitored projects
- 5-minute check intervals
- Email alerts
- Public status pages
- 30-day data retention

### Team ($15/month)
- 20 monitored projects
- 1-minute check intervals
- Email + SMS alerts
- Custom domains
- 90-day data retention
- Incident management
- Multi-user access

### Enterprise ($49/month)
- Unlimited projects
- 30-second check intervals
- All alert channels
- Custom integrations
- 1-year data retention
- API access
- Priority support

## Competitive Analysis

### StatusPage.io (Atlassian)
- **Price:** $29-79/month
- **Pros:** Trusted brand, Atlassian integration
- **Cons:** Expensive for solo devs, complex UI

### UptimeRobot
- **Price:** Free (50 monitors), $7/month (pro)
- **Pros:** Generous free tier
- **Cons:** Dated UI, limited customization

### Better Stack (Uptime)
- **Price:** $18/month
- **Pros:** Modern UI, good alerting
- **Cons:** No free tier, focused on teams

### BetterUptime
- **Price:** $20+/month
- **Pros:** Beautiful UI, incident management
- **Cons:** Expensive, overkill for solo devs

### Your Advantage
- **Built for solo devs** - Simple, focused, affordable
- **Beautiful UI** - Modern design, fast
- **Subdomain status pages** - Easy sharing
- **Dogfooded** - You use it daily for your projects
- **Price:** $5-15/month vs $20-79/month

## Next Steps

1. **Validate personal need**
   - How often do your projects actually go down?
   - Would you check this dashboard daily?
   - What alerts do you actually want?

2. **Choose tech stack**
   - Convex vs Supabase?
   - QStash vs other cron service?
   - Email provider?

3. **Design UI**
   - Sketch dashboard layout
   - Status page design
   - Mobile-first?

4. **Build MVP**
   - 2-3 weeks part-time
   - Ship and dogfood
   - Iterate based on usage

5. **Decide on product**
   - After using for 1-2 months
   - Does it solve a real problem?
   - Would others pay for it?

## Notes

- Start as personal tool, validate by using it
- If it's valuable to you, it's valuable to other solo devs
- Market is crowded but mostly enterprise-focused
- Solo dev niche ($5-15/month) is underserved
- Could be profitable side business at 100-200 customers
- Alternative: Just keep it personal and open source it

---

**Created:** 2025-11-01
**Last Updated:** 2025-11-01
