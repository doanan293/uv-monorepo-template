## Prompt Guideline (agent & harness)

Write, review and tune every prompt (system prompt, sub-agent prompt, judge prompt, tool description) using the template and rules below. The goal is prompts that are short, generalize well and are cache-friendly, because long prompts or prompts fitted too closely to test cases lower quality on new inputs and raise cost.
The numbers in this guideline are starting values that have not yet been validated by the team's evals; adjust them based on evals and record the reason in the PR.

### 1. Template

Use this template. The `<!-- -->` comments are filling instructions; delete all of them when writing the real prompt, because comments cost tokens and lengthen the static part.

```
<role>
<!--
Fill in this pattern: "You are {role}, serving {audience}, in the context of {product/system}."
Illustration (do not copy): "You are an intent classifier, serving the router of a customer-support agent, in the customer-care system of store X."
Keep the role functional, because the role mainly shapes tone/format/behavior; correctness comes from context and constraints. There is no evidence that an expert persona improves accuracy, and it can lower accuracy on knowledge tasks.
Recall/reasoning/code/classification/extraction tasks: keep the role minimal and put the content in <input> and <constraint>.
Keep the role in the same domain as the task, because an off-domain role can lower accuracy or cause refusals.
Put rules in <constraint> so each tag has exactly one function.
-->
</role>

<task>
<!--
Write 1–3 sentences: what to do and what the result is used for.
Write it like briefing a capable new hire who knows nothing about the project, because the model does not have your context.
Start with a verb that states the job (Classify / Extract / Write / Evaluate), because the first sentence determines how the model understands the work.
State where the result is used, because knowing where the result goes helps the model choose the necessary level of detail and format.
Illustration (do not copy): "Classify the customer message into exactly one intent so the router can pick the handling tool."
-->
</task>

<context>
<!--
Optional: drop this tag when <task> is already self-sufficient.
Holds stable background the model needs and cannot infer: domain, business constraints, internal terms/conventions (explain what each term means).
Add a piece of information only when the model fails without it, because long context raises cost and dilutes the instructions.
Keep it at the domain level. Per-request data goes in <input>, because context is part of the static part and must stay identical across requests to be cached (section 3).
Keep eval data (IDs, names, wording from test cases) out of context (see section 2.3).
-->
</context>

<instruction>
<!--
Describe how to do the work and what the output must achieve.
Write the processing steps as a numbered list when order matters (a later step depends on an earlier one's result) or the problem is complex (debugging, decision-making, multiple perspectives). Use bullets for independent requirements; write 1–2 sentences for a simple task.
State the quality criteria, format and required parts of the output (length, structure, tone) as measurable criteria. Replace vague words like "good", "complete", "appropriate" with something concrete (e.g. "summarize in 3 sentences" instead of "summarize fully"), because every person and every model reads these words differently.
Agent/harness: state when to call which tool (details belong in the tool description), the stop condition, and what to do when information is missing or a tool fails (e.g. report what is missing).
Write zero-shot; the conditions for adding examples are in section 2.1.
-->
</instruction>

<constraint>
<!--
Each bullet is one sentence that can be checked pass/fail.
Describe the desired behavior. E.g. "Write in flowing paragraphs" instead of "Do not use markdown".
Add a short reason to each rule so the model applies it correctly in situations not listed. E.g. "Do not use ellipses because the output is read by TTS". Skip the reason for obvious rules.
Use a normal voice, no capitals or MUST/NEVER, because newer models follow prompts closely and over-emphasis easily makes a rule over-applied. For an important rule, state the consequence of violating it.
Tasks that rely on facts or input data: allow the model to say "I don't know", e.g. "When unsure or missing information, say so instead of guessing (because the output is used to make decisions)". Tasks that use the given context: "Only use information in <input>".
Each rule lives in one place; content already in <instruction> is not repeated here.
-->
</constraint>

<!--
Optional: <example><sample_input>...</sample_input><ideal_output>...</ideal_output></example>
Place after <constraint>; add only under the conditions in section 2.1.
-->

<input>
<!--
Holds the data that changes per request, placed last (reason in section 3).
Wrap each variable in a descriptively named tag (<ticket_content>, <chat_history>, <tool_result>), because a specific name tells the model the data's role.
Put behavioral instructions in <instruction> and <constraint>, because <input> is data; mixing them makes it hard for the model to tell instructions from data.
-->
</input>
```

The order is fixed. The static part (`role` → `task` → `context` → `instruction` → `constraint` → example if any) goes on top, the dynamic part (`input`) at the very bottom.
Each tag answers one question, and each piece of information lives in only one tag:
- `role`: who, serving whom, where
- `task`: what to do, what the result is used for
- `context`: stable background
- `instruction`: how to do it, what the output looks like
- `constraint`: boundaries and standards
- `input`: the request's data

### 2. Keep prompts short and general

1. **Write rules per failure class.** A rule per individual failure only fixes that test case and breaks on new inputs. Check: remove proper names/IDs/specific values from the rule and it still makes sense.
2. **Tie every new rule to evidence** (starting value: ≥2 distinct failing cases, or 1 real production failure mode) and record it in the PR, to avoid adding rules from a single observation.
3. **Keep eval data out of the prompt:** IDs, names, wording, figures from the dataset, and if-else on specific inputs. Copying them into the prompt inflates the eval score without improving real inputs.
4. **Default to zero-shot.** The conditions for adding examples are in section 2.1.
5. **Keep the static part lean** (starting value: `constraint` ≤ ~10 bullets, total static part including `task` and `context` ≲ 1500 tokens), because long prompts raise cost and latency and make overlapping rules hard to debug. If you exceed the threshold, explain why in the PR. Every rule added comes with merging/dropping another rule, or proof that the new rule is worth it.
6. **Push what code can control** (schema, length, format) into validation/structured output, because code guarantees it more reliably than a reminder and shortens the prompt.

#### 2.1 When to add examples

Examples are the biggest overfitting risk because models tend to follow or copy them closely. Add an example only when all 3 conditions hold:

1. **Zero-shot has hit its ceiling:** a zero-shot baseline exists, `instruction`/`constraint` have been clarified, and the failure mode still recurs.
2. **The failure is hard to put into words:** corner cases or ambiguous inputs (e.g. sarcasm, the boundary between 2 close labels), tone/style that is hard to describe, or complex formats the schema cannot handle yet.
3. **Evals prove it helps:** the score improves on both dev and held-out.

Use a `constraint` instead of an example when the rule fits in one sentence, when only a single failing case needs fixing, when the format is already guaranteed by schema/validation, or when the task leans on recall/reasoning (examples make the model follow the pattern instead of reasoning).

Once the conditions are met:
- Tie each example to a specific failure mode; record the failure mode and before/after scores in the PR.
- Use at most 3 examples (starting value), covering diverse cases, taken from outside the eval set used for scoring.
- Add 1–2 sentences explaining why the `ideal_output` is good.
- Count examples toward the static part's length budget.
- When switching models or editing instructions, try removing each example; if the score does not drop, delete it.

### 3. Maximize cache hits

Caching works by prefix, processed in the order tools → system → messages. The cache is only used when the content up to the breakpoint is identical; adding the single word "please" is enough to lose it.

- Put the static part (`role/task/context/instruction/constraint/example`) first and `<input>` last.
- Move volatile values (timestamp, current date, request/session ID, user name, UUID, random) into `<input>`, because they change the prefix on every request.
- Serialize deterministically: sorted JSON keys, lists/sets in a fixed order.
- Keep tool definitions identical in content and order; changing tools mid-session invalidates the cache for everything after them.
- Agent loop: only append to the history, never edit or insert into already-sent turns. Put a breakpoint at the end of the latest message so the history gets cached incrementally.
- Use at most 4 breakpoints (`cache_control: {"type": "ephemeral"}`), prioritizing the end of tools/system (changes least), then the end of the history.
- Make sure the cached part is ≥1024 tokens (check the docs of the model in use). The default TTL is 5 minutes (a 1-hour option exists at a higher write price), so caching only pays off when the prompt is called repeatedly within the TTL.
- Batch static-prompt edits into one change, because each edit causes one cache miss.
- Verify via `cache_creation_input_tokens` and `cache_read_input_tokens` in `usage` (check field names against the current API docs); a repeated request with `cache_read` = 0 means it is missing.

### 4. Tuning process (with evals)

1. Set the goal and the grading criteria (model-based or code-based).
2. Write the first prompt and run evals to get a baseline.
3. Change one thing at a time, then re-run evals. Technique order: clear/direct → specific (guidelines and steps) → XML structure → examples (per section 2.1).
4. A/B the role: compare with a role vs. without (or a minimal role). Keep the role if the score does not drop.
5. Develop with 2–3 cases for speed; when finalizing, run the large dataset + held-out set.
6. Keep a change when the score improves on both dev and held-out; a held-out drop means overfitting, so revert.
7. Try removing each rule and each example; drop those whose removal leaves the score unchanged.
8. When a rule is over-applied, soften it before deleting it (remove emphasis, add a reason and scope, rewrite it as desired behavior), then re-run evals.
9. Record in the PR: before/after scores, number of cases, rules added/removed and the evidence.
