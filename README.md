# RAGBench — Advanced RAG Evaluation Framework

A proposed evaluation framework for teams comparing retrieval-augmented generation pipelines. It would help distinguish retrieval failures from generation failures when changing document chunking, retrieval depth, reranking, or prompts.

The main scenario is a comparison of candidate pipelines on the same versioned question set and document collection, with evidence retained for each answer.

**Status: Concept — implementation is not included in this repository.** No evaluation engine, model integration, dataset, or benchmark results are provided.

## Proposed Workflow

1. Prepare a fixed corpus and question set. Each question should include relevant document or passage IDs, an expected answer where appropriate, and an answerability label.
2. Run each pipeline configuration against that same corpus snapshot. Record retrieved passages, their ranks, the final context, generated answers, and citations.
3. Score retrieval and generation separately. Review failures before attributing an aggregate improvement to a particular component.
4. Compare quality with latency and token usage. Export aggregate metrics together with question-level evidence and configuration identifiers.

## Proposed Design

A small experiment runner would connect dataset loading, a pipeline adapter, metric functions, and a comparison report. Pipeline adapters would expose intermediate context instead of returning only final answers.

Retrieval evaluation would use Recall@k for relevant-evidence coverage, MRR for the first relevant result, and nDCG@k when graded relevance labels exist. Generation assessment would examine answer correctness, support from supplied context, citation accuracy, and behavior on unanswerable questions.

Reference-based scores, human judgments, and optional model-based judgments would remain distinguishable. A judge's model version, prompt, and scoring rubric would accompany its output; an automated judgment would not be treated as ground truth.

## Illustrative Example

Question: “Can a customer return an opened item?” A policy corpus contains an exception clause and an unrelated shipping page.

If the exception clause is absent from retrieved results, the failure is retrieval-related. If the clause is present in the final context but the answer contradicts it, the failure is generation-related. This example illustrates the intended diagnosis, not an observed run.

## Scope & Limitations

The initial concept concerns text documents and offline comparisons. Relevance labels can be incomplete, equivalent passages can complicate matching, and model judges can be inconsistent. Comparisons would require a consistent corpus, relevance unit, and evaluation budget. No live connector, vector database, or hosted service is assumed.
