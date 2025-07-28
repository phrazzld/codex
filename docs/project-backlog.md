# PROJECT BACKLOG

## ACTIVE

- **misty step marketing site**
  - tight, punchy, elegant
  - testament to ui/ux/design/our aesthetic
  - focus on consulting and development services:
    - integrating ai into your business
    - staff augmentation
    - building ai-powered features
    - streamlining operations with ai tools and custom software
    - etc

- **thinktank**
  - cli for sending arbitrary instructions and context to an arbitrary set of llm models
  - automatically synthesize their outputs to "wisdom of crowds" the llms

- **switchboard**
  - rust cli for proxying claude code
  - see the requests and responses and activity
  - ultimately intercept and manipulate, enable hijacking requests that would be going to anthropic to go to other providers
  - sanity check requests and responses more easily with custom middleware

- **scry**
  - anki killer
  - ai-enhanced srs
  - go api, react native mobile app
  - ux: user captures "memos", tidbits they want to remember
  - we automatically transform those tidbits into large sets of quizzes -- multiple choice questions for now, but ultimately free response questions and other quiz types
  - user is always reviewing -- core ui is review and everything else punches out from there
  - user, during a review, can add a memo, postpone the current item, edit the current item, delete the current item, or generate more items like it (eg more but easier, more but harder)

- **gitpulse**
  - github app, get quantitative and qualitative analysis of github activity across your repositories, organizations, contributors
  - use ai to see more than "number of commits" -- get deep understanding of who knows what how well what *kind* of work has been done, etc
  - good for individual contributors to get an understanding of what they've been doing
  - good for managers to see what their team has been doing
  - ultimately integrate with project management software etc to make assigning work easier, create visibility into dev velocity, etc

- **brainrot publishing house**
  - comedic yet faithful terminally online zoomer brainrot translations of classic public domain works
  - graphic novelizations
  - brainrot cliffnotes of authors, series, subjects
  - in general: ai-enhanced culture/media/publishing company

- **time is money**
  - chrome extension for seeing prices as hours of work
  - needs some polish and upgrades to stay alive
    - v3 manifest migration
    - new web store assets
    - fresh coat of paint in the ui

## TT-REVIEW SYSTEM ENHANCEMENTS

### High Priority (Next Sprint)
- **Add BATS test suite** for core functions in tt-common.sh
  - Test tt_execute_thinktank, tt_handle_output, argument parsing
  - Mock thinktank calls for unit tests
  - Add integration tests for full workflow
  - *Rationale*: Shell scripts are critical for CI/CD but harder to test
  - *Effort*: Medium (2-3 days)
  - *Reference*: PR #13 code review

- **Make output parsing more robust** (bin/tt-common.sh:225)
  - Replace brittle regex with JSON parsing if thinktank supports it
  - Add multiple fallback patterns for different versions
  - *Rationale*: Current parsing is fragile and could break with thinktank updates
  - *Effort*: Low (1 day)

- **Standardize argument handling patterns**
  - Some scripts use tt_setup_diff_review, others parse manually
  - Create consistent approach across all scripts
  - *Rationale*: Inconsistency makes maintenance harder
  - *Effort*: Low (1 day)

- **Dynamic review discovery in synthesis** (bin/tt-review-synthesis:35-58)
  - Replace hardcoded file list with: `find . -name "CODE_REVIEW_*.md"`
  - *Rationale*: Manual maintenance required when adding new review types
  - *Effort*: Low (few hours)

### Medium Priority (Technical Debt)
- **Add parallel review execution option**
  - Run multiple reviews concurrently for faster results
  - *Rationale*: Sequential execution is slow for full reviews
  - *Effort*: Medium (2 days)

- **Optimize large diff handling** 
  - Stream processing instead of loading all into memory
  - *Rationale*: Current approach could fail on very large PRs
  - *Effort*: Medium (1-2 days)

- **Add configuration file support**
  - Allow .tt-review.yml for project-specific settings
  - *Rationale*: Hard-coded values limit flexibility
  - *Effort*: Medium (2 days)

- **Improve error message consistency**
  - Standardize error format and logging levels
  - *Rationale*: Better debugging and user experience
  - *Effort*: Low (1 day)

## backburner

- **ai real estate property staging**
  - input: photos of empty rooms, moods (or buyer personas)
  - output: high quality photorealistic targeted staged photos

- **ai app store promo image generator**
  - take app name, context blob about what it does who it's for etc
  - output comprehensive app store listing assets

- **resumake**
  - ai powered resume generator
  - upload context, eg old resume, stream of consciousness about your professional history and situation, maybe job listing of job you're targeting
  - we generate clarifying questions for you to answer
  - then we synthesize into a base cv -- comprehensive, long, exhaustive -- as well as a targeted resume -- tight, punchy, derived from the cv, focused on your job description
  - probably all markdown to start
  - ultimately break out into more customization, but keep it simple clean elegant

- **glance**
  - script for generating ai summaries of your project
  - starts at the deepest directory, generates a glance.md file of the contents of that directory, works its way up (to mitigate context window length). if current directory contains a directory, use that directory's glance.md file instead of its contents -- results in a whole project full of glance files, each with great context

- **handoff**
  - easily grab a full directory worth of content and put it on your clipboard or in an output file, formatted with context tags

- **vanity**
  - personal website
  - show quotes i like, books i've read and am reading, map of where i've been, projects i've built, etc

- **phone dermatologist**
  - basically version control photos of your skin
  - ai analyzes changes, suggests visiting proper dermatologist when risk threshold gets crossed

- **superwire**
  - meridian competitor: news aggregator / personalized intelligence briefing
  - anyzine
  - autogen political cartoons
  - you are borderline retarded aka devil's advocate

- **sous, chefbot**
  - ai personalized recipe exploration

- **rolodex**
  - "growth diary" for relationships
  - chat about each of your relationships
  - log what you know about each person and when you speak / engage
  - get insights and reminders, suggested check-ins and activities, etc

- **bitcoin wallet**

- **white hat bitcoin self audit deanonymizer for privacy**

- **claude run web server**
  - accepts user inputs for feature requests
  - let ai loose on a server and have it try to maintain itself and generate revenue and build new features etc

- **stylish book tracker**

- **timeline creator**

- **family tree creator**

- **simple fitbod / seven minute workout app replacement**

- **simplified trimmed down hallow replacement**
  - just core prayers, with audio: liturgy of the hours, rosary

- **intellectual arena game / debate gym**
  - take a position (or get assigned one)
  - some kind of clocked urgent "respond to this point" or "take down this attack" thing
  - maybe multiplayer

- **famous speeches app**

- **accountabilibuddy chatbot**

- **hos**
  - reclaim.ai competitor, calendar / todo list integration that manages your schedule and todo list for you

- **bucket list helper**

