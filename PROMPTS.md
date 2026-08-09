# User Prompts

## Prompt 1


## Prompt 2


## Prompt 3
Continue

## Prompt 4
give commit message

## Prompt 5
now what to do

## Prompt 6
test the backend server it is not working

## Prompt 7
test the backend server it is not working

## Prompt 8
now what to do

## Prompt 9
now how to test the model

## Prompt 10
i am using postman for sending post requests, tell according to this
why to integrate open ai api keys thats not free

## Prompt 11


## Prompt 12
give commit message

## Prompt 13
Continue

## Prompt 14
give commit message

## Prompt 15
now can you access another branch on which i am working right now

## Prompt 16
update readme.md in this branch according to changes made in this branch

## Prompt 17
right now rashi_work have updated code for both fronted and backend , now test code on this branch why agent initialisation is not woking using frontend

## Prompt 18
do you added apis for fetching live data from internet

## Prompt 19
why ai security agent opening automatically, on live dashboard there is no live news data shown everything is shown zero, check out whats wrong in code

## Prompt 20
give commit message

## Prompt 21
You are acting as an extremely strict senior hackathon judge, production AI engineer, backend architect, security reviewer, and QA engineer.

Your job is NOT to help me build the project initially.

Your job is to AUDIT, TEST, BREAK, and SCORE the CURRENT WORKING PROJECT exactly as a real judge would for the ABTalks Vibe Code Hackathon.

Assume hundreds of competent teams have submitted.

Do not give bonus points for:
- effort
- fancy UI
- large codebase
- number of technologies
- AI-generated architecture
- features mentioned only in README
- features that exist in code but do not actually work

Give credit ONLY for behavior you can verify from the running application, API, codebase, database behavior, logs, tests, and autonomous execution.

Be skeptical.

==================================================
HACKATHON PROBLEM STATEMENT
==================================================

We are submitting for:

PS3 — AUTONOMOUS AI CREATOR

The goal is to build an autonomous AI and technology persona that, after ONE initialization request:

1. Independently discovers topics from live information sources.
2. Decides which topics are worth publishing.
3. Intentionally rejects weak/unworthy topics.
4. Maintains a consistent persona/editorial voice.
5. Remembers previously published content.
6. Avoids unnecessary repetition.
7. Continues operating over time without additional human prompts.
8. Publishes new posts autonomously.
9. Provides transparent publishing rationale.
10. Provides sources used for every published post.

The agent must remain focused on AI and technology.

Real social-media posting is NOT required.

==================================================
MANDATORY API CONTRACT
==================================================

The evaluator calls initialization exactly once:

POST /api/agent/init

Example body:

{
  "persona": {
    "name": "Ada",
    "domain": "AI Security"
  }
}

Expected response:

{
  "agentId": "abc-123"
}

After initialization, the ONLY evaluator endpoint used is:

<truncated 17983 bytes>
 preserve opinions?

# 11. PERSONA AUDIT

Is this genuinely a persistent identity or only a system prompt?

Give examples.

# 12. SOURCE / HALLUCINATION AUDIT

Report:

Source quality
Citation reliability
Unsupported claims
Prompt-injection risk

# 13. 48-HOUR FAILURE ANALYSIS

List every realistic reason the autonomous system might stop producing valid output during judging.

# 14. LIVE STEER READINESS

Rate /10.

Provide five likely surprise requests and expected implementation difficulty.

# 15. TOP 10 THINGS PREVENTING US FROM WINNING

Rank from most damaging to least damaging.

Do NOT include generic advice.

Reference actual code/features/behavior.

# 16. HIGHEST-ROI FIXES BEFORE SUBMISSION

Assume very limited remaining hackathon time.

Group fixes into:

DO NOW
NEXT
ONLY IF TIME

Give estimated implementation time for each.

# 17. RETEST PLAN

Give exact commands/API requests/tests I should run after fixes.

# 18. FINAL JUDGE DECISION

If you were one of the two official judges:

Would you put this project in the Top 6?

YES / NO / BORDERLINE

Explain in no more than 5 sentences.

==================================================
IMPORTANT BEHAVIOR
==================================================

Do not start fixing the project until the complete audit is finished.

First:
UNDERSTAND → RUN → TEST → BREAK → SCORE → REPORT

Only after producing the full judging report, ask me whether I want you to begin fixing issues.

Do not soften criticism.

Do not praise implementation unless verified.

Do not assume README claims are true.

Do not mark a requirement complete merely because a class/function with the correct name exists.

Test actual behavior.

If something cannot be tested because credentials/services are missing, label it:

UNVERIFIED

not:

WORKING.

Start by inspecting the complete repository and explaining the architecture you found in 10–15 lines.

Then begin the audit.

## Prompt 22
first give commit message for remaining commits

## Prompt 23
on github everything is seems to be fine, but in git check there are a lot of merge conflicts

## Prompt 24
now on which branch updated code is

## Prompt 25
give commit message

## Prompt 26
now i merged all code of rshi_work into main branch, now checkout it have some problem on main branch

## Prompt 27
i have created a branch abhinav_work, now implement all these new features in this new branch

## Prompt 28
now check .gitignore does it have everything that dont need to be push on github,

## Prompt 29
in this project can we create agent from any domain or it has some limited list in backend

## Prompt 30
does these changes of gitignore merged into all branches

## Prompt 31
merge abhinav_work latest codes into main

## Prompt 32
now tell me in easy words what this project is doing

## Prompt 33
so i have to wait for 30 minutes to see a post

## Prompt 34
where is .env

## Prompt 35
it shows post only agent intialisation, after that it is not posting after 1 min

## Prompt 36
merge updated code of abhinav_work into akshat_dev

## Prompt 37
why it is not posting 2nd post after 1 minute, check out the issue and fix it in a loop until it works as required

## Prompt 38
still no post after 1 min

## Prompt 39
it is giving same post again and again

## Prompt 40
it is giving same post again and again

## Prompt 41
Continue

## Prompt 42
now test it on 10 different roles run for 10m minutes each , then test the quality of posts created by agents , then show mme stats and judge the model based on performanxce, accuracy etc

## Prompt 43
continue remining testing

## Prompt 44
now suggest improvements in ui, that will make it easy for judges to use, what changes can we made in ui so it will have a very good impression on judges. just discuss dont implement

## Prompt 45
update .gitignore accordingly ,
now i have switched to new branch ui_work,
now implement all above discussed ui improvements in this new branch

## Prompt 46
branch UI_work,
procced with implementation

## Prompt 47
on ui i think we should show list of roles for which our project perform good during agent intinalisation, if judges want they can mmanually type there custom role

## Prompt 48
no post appearing

## Prompt 49
in which branch you have made above chnages?

## Prompt 50
now work on akshat_dev,
Fix the current autonomous AI persona backend. Do NOT rewrite the whole project. Modify the existing implementation to solve the following three problems.

============================================================
PROBLEM 1 — OLD RUN DATA IS CONTAMINATING NEW AGENTS
============================================================

The PostgreSQL database currently persists posts, topics, rejected topics, and memory from previous backend runs.

When I stop and restart the backend and initialize a new agent, the new agent is sometimes treating posts/topics from the previous run as already published/discussed.

Example:

Previous backend run:
Agent A publishes:
"OpenAI releases X"

Backend is stopped.

New backend run:
POST /api/agent/init
creates Agent B.

Agent B discovers a new topic.

The editorial engine incorrectly considers it already discussed because data from Agent A or the previous test run still exists.

FIX THIS CORRECTLY.

IMPORTANT:

DO NOT simply delete the entire database whenever the FastAPI server starts.

The evaluator needs persistence during the same agent's lifetime.

The correct lifecycle is:

Server starts
    ↓
Existing database remains intact
    ↓
POST /api/agent/init
    ↓
Create a NEW agentId
    ↓
This agent starts with CLEAN editorial memory
    ↓
All future posts/memory belong to this agentId
    ↓
Server restart
    ↓
Same agent data remains persisted

============================================================
AGENT-SCOPED MEMORY
============================================================

Every memory lookup must be scoped to the current agentId.

When checking:

- previously published posts
- published topics
- duplicate URLs
- duplicate titles
- semantic similarity
- rejected topics

ONLY consider records belonging to the current agent.

Never perform a global query such as:

SELECT * FROM posts

and then use those posts as memory for the current agent.

Instead use:

SELECT * FROM posts WHERE agent_id = current_agent_id

T
<truncated 11503 bytes>
-------------------------------

Test 3:

Create:

domain = "AI Security"

The agent should prefer:

- prompt injection
- jailbreak research
- AI vulnerabilities
- agent security
- model security
- AI supply-chain attacks
- defensive AI research

It should reject unrelated technology news.

------------------------------------------------------------

Test 4:

Initialize ONCE.

Wait one scheduler cycle.

GET /feed.

Expected:
1 post.

Wait another minute.

GET /feed again.

Expected:
2 posts, assuming another suitable topic exists.

The second post must be generated by the scheduler.

GET /feed must not create it.

------------------------------------------------------------

Test 5:

Restart server WITHOUT creating a new agent.

The existing agent's posts must still exist.

The existing agent's memory must still exist.

The scheduler must continue using that agent's persisted memory.

============================================================
FINAL OUTPUT
============================================================

After modifying the code, provide:

1. Files changed.
2. Explanation of the old bug.
3. Explanation of the new agent-scoped memory behavior.
4. Explanation of the persona relevance gate.
5. Explanation of the new duplicate detection.
6. Explanation of the scheduler behavior.
7. Example logs showing irrelevant topics being rejected.
8. Example logs showing relevant topics being published.
9. Example API response with clean raw source URLs.
10. Commands to test the complete flow.

Do NOT rewrite unrelated working components.

Do NOT solve the problem by deleting the database on every server startup.

The final system must satisfy:

NEW AGENT = CLEAN MEMORY

SAME AGENT = PERSISTENT MEMORY

IRRELEVANT TOPIC = REJECT

RELEVANT TOPIC = CAN PUBLISH

PREVIOUSLY PUBLISHED TOPIC = REJECT

RELATED BUT DISTINCT TOPIC = CAN PUBLISH

POST GENERATED ONLY BY AUTONOMOUS SCHEDULER

GET /feed = READ ONLY

## Prompt 51
continue remaining work

## Prompt 52
give commit message

## Prompt 53
why there is no post for devops

## Prompt 54
you have to create a PROMPTS.md file and write all my prompts
on main branch

