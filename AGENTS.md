# Agent Instructions for Codex

This repo builds an acquisition lead-generation research pipeline.

## Non-negotiable rules

1. Do not make unsupported factual claims.
2. Every score must include evidence and confidence.
3. Prefer small, testable modules over one large agent.
4. Never scrape sources in violation of robots.txt, terms of service, or applicable law.
5. Outputs are estimates, not facts.
6. Use ranges for revenue and cashflow.
7. Avoid language like "desperate," "vulnerable," or "easy target." Use "estimated openness to acquisition discussion" or "transition likelihood."
8. Do not infer sensitive personal attributes unless directly supported by public business context and necessary for commercial analysis.
9. Keep connector code behind interfaces so sources can be swapped.
10. Preserve source URLs, retrieval timestamps, and raw evidence where possible.

## CSV output contract

Every CSV row should include at minimum:

- business_name
- business_type
- address
- website
- county
- state
- activity_score
- activity_trend
- activity_confidence
- estimated_revenue_low
- estimated_revenue_high
- estimated_cashflow_low
- estimated_cashflow_high
- cashflow_confidence
- transition_likelihood
- transition_score
- likely_transition_driver
- transition_confidence
- acquisition_narrative
- evidence_urls
- notes

## Development guidance

When asked to add a feature:

1. Add or update schemas first.
2. Add fixtures if needed.
3. Implement deterministic logic.
4. Add tests.
5. Only then add LLM-assisted summarization or extraction.

Do not hide uncertainty. Use confidence fields and notes.
