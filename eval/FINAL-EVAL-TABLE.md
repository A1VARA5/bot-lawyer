# Bot Lawyer, final eval table

40 questions, one row each, using the best available final result per question: q01 to q18 are the run 2 verdicts from `GRADES-2.md` (the run that died at q19 when the model key ran out of credit), q19 to q33, u01 to u03 and k01 to k04 are the run 3 verdicts from `GRADES-3.md`. Seconds and tools come from the same run as the verdict (`eval/results.json` for run 2, `eval/results-run3.json` for run 3). Verdict rules: PASS needs the right ruling, at least one source URL and an effective date, and for traps no fall to the stale answer; unknowns pass only if the agent admits the gap and invents nothing; the two drafts pass only as a single md code block plus one Length line; the four kb items pass only if the answer used the knowledge base and says something the rules dataset alone could not. PARTIAL is a right ruling with a required element missing or hedged. FAIL is a wrong ruling, an invented fact, or a trap taken.

| id | area | kind | verdict | seconds | tools used |
|---|---|---|---|---|---|
| q01 | intents | trap | PASS | 15.1 | 1 groq_query |
| q02 | intents | trap | PASS | 16.0 | 1 groq_query |
| q03 | intents | trap | PARTIAL | 13.4 | 1 groq_query |
| q04 | intents | trap | PASS | 15.6 | 1 groq_query, 1 knowledge_base_read |
| q05 | intents | standard | PASS | 13.0 | 1 groq_query |
| q06 | verification | trap | PASS | 18.0 | 1 groq_query |
| q07 | verification, age | standard | PASS | 10.4 | 1 groq_query |
| q08 | ownership | trap | PASS | 11.6 | 1 groq_query |
| q09 | rate limits | trap | PASS | 11.4 | 1 groq_query |
| q10 | rate limits | standard | PASS | 12.0 | 1 groq_query |
| q11 | rate limits | standard | PASS | 13.0 | 1 groq_query |
| q12 | data retention | standard | PASS | 16.0 | 1 groq_query |
| q13 | data retention | standard | PASS | 12.0 | 2 groq_query |
| q14 | data retention | standard | PASS | 12.6 | 1 groq_query |
| q15 | data retention | standard | PASS | 32.4 | 2 groq_query, 1 knowledge_base_read |
| q16 | monetisation | standard | PARTIAL | 10.6 | 1 groq_query |
| q17 | monetisation | standard | PASS | 11.4 | 1 groq_query |
| q18 | monetisation | standard | PARTIAL | 19.6 | 1 groq_query |
| q19 | monetisation | trap | PASS | 25.4 | 1 groq_query, 1 knowledge_base_read |
| q20 | app directory, verification | standard | PASS | 33.9 | 2 groq_query, 1 knowledge_base_read |
| q21 | verification | standard | FAIL | 23.1 | 1 groq_query, 1 knowledge_base_read |
| q22 | rate limits, oauth | standard | PASS | 25.0 | 1 groq_query, 1 knowledge_base_read |
| q23 | tokens and security | standard | PASS | 21.9 | 1 groq_query, 1 knowledge_base_read |
| q24 | intents, data retention | standard | PARTIAL | 32.1 | 1 groq_query, 1 knowledge_base_read |
| q25 | data retention | standard | PASS | 28.0 | 2 groq_query, 1 knowledge_base_read |
| q26 | formatting | standard | PASS | 23.9 | 1 groq_query, 1 knowledge_base_read |
| q27 | formatting | standard | PASS | 23.1 | 1 groq_query, 1 knowledge_base_read |
| q28 | formatting | standard | PASS | 22.0 | 1 groq_query, 1 knowledge_base_read |
| q29 | formatting | standard | PASS | 27.6 | 2 groq_query, 1 knowledge_base_read |
| q30 | formatting | standard | PASS | 23.4 | 1 groq_query, 1 knowledge_base_read |
| q31 | formatting | standard | PASS | 24.0 | 1 groq_query, 1 knowledge_base_read |
| q32 | formatting (draft) | standard | PARTIAL | 19.0 | 1 groq_query |
| q33 | formatting (draft) | standard | PARTIAL | 18.0 | 1 groq_query |
| u01 | verification | unknown | PASS | 32.6 | 1 groq_query, 1 knowledge_base_read |
| u02 | data retention | unknown | PARTIAL | 31.4 | 2 groq_query, 1 knowledge_base_read |
| u03 | intents | unknown | PASS | 22.0 | 1 groq_query, 1 knowledge_base_read |
| k01 | data retention (kb) | standard | PASS | 28.6 | 1 groq_query, 1 knowledge_base_read |
| k02 | intents (kb) | standard | PARTIAL | 25.9 | 1 groq_query, 1 knowledge_base_read |
| k03 | tokens and security (kb) | standard | PASS | 24.1 | 1 groq_query, 1 knowledge_base_read |
| k04 | monetisation (kb) | standard | PASS | 25.6 | 1 groq_query, 1 knowledge_base_read |

## Totals

| | PASS | PARTIAL | FAIL | items |
|---|---|---|---|---|
| trap | 7 | 1 | 0 | 8 |
| standard | 22 | 6 | 1 | 29 |
| unknown | 2 | 1 | 0 | 3 |
| **all** | **31** | **8** | **1** | **40** |

- 31 of 40 PASS (77.5 percent), 8 PARTIAL, 1 FAIL. Counting PARTIAL as a right ruling with a gap, the ruling line was right on 39 of 40; the one FAIL (q21) also had the right ruling but put a sentence that is not on the cited page inside a blockquote.
- No trap item fell for its stale answer in any run (8 of 8).
- Average 20.6 s per answer across the 40 (run 2 items 14.7 s, run 3 items 25.5 s; the run 3 items nearly all read the knowledge base as a second step).
- 68 tool calls in total, 46 groq_query and 22 knowledge_base_read; 22 of 40 answers read the knowledge base.
- The 8 PARTIALs: q03 (90 day window tied to the wrong trigger), q16 (asked for the region instead of ruling both branches), q18 (checklist truncated), q24 (garbled source title and truncated URL), q32 and q33 (Length line miscounted; q33 also narrated before the fence), u02 (fell back to the purpose clause rather than the deletion duty), k02 (quoted the review guide instead of the announcement).
- Earlier runs, for the record: run 1 was 23 PASS / 5 PARTIAL / 0 FAIL on 28 items before the situation block was sent; run 2 reran the first 18 with the situation block and fixed q01, q04 and q12; k01 in run 3 was empty on its first pass (output cap of 1400 tokens) and was rerun once after the cap went to 3000.

## How this eval was made

The 40 questions were written by us, from our own research into Discord's developer docs, developer support articles, policy pages and change log, together with the expected answers they are graded against; the trap and unknown items were built around contradictions we had already found between those pages. Each answer was graded by a separate model agent (not the one answering) against the expected answer, expected rules and note, with strict marking, and the grades were spot checked by a human, including checks of quoted text against the raw page snapshots. This is not an independent benchmark: the people who wrote the questions also built the dataset the agent queries, so it measures whether the agent reads the structure correctly, not whether the structure is complete or right. The answering model was Claude Sonnet, called through the Vercel AI SDK, with tool access to two Sanity Context MCP endpoints, one over the rules dataset (GROQ queries) and one over the knowledge base of page snapshots. Runs were made against the local build on 2026-09-19; nothing in the answers was edited after the fact, and the one rerun (k01) is noted above.
