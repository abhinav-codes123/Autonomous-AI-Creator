"""Prompt Builder module for structured LLM generation prompts."""

import json
from app.services.discovery.base import TopicData
from app.services.persona.persona_engine import PersonaProfile


class PromptBuilder:
    """Constructs structured, persona-aligned prompts for LLM post generation."""

    def build_post_generation_prompt(
        self,
        persona: PersonaProfile,
        topic: TopicData,
        previous_posts: list[str],
    ) -> str:
        prev_posts_str = "\n".join(f"- {post[:150]}..." for post in previous_posts) if previous_posts else "None yet."
        style_rules = "\n".join(f"- {rule}" for rule in persona.style_guidelines)
        keywords_str = ", ".join(persona.keywords)

        prompt = f"""You are {persona.name}, an autonomous AI expert specializing in {persona.domain}.

## Persona Profile
- Name: {persona.name}
- Domain: {persona.domain}
- Tone: {persona.tone}
- Domain Keywords: {keywords_str}
- Editorial Opinions: {persona.editorial_opinions}

## Writing Style & Constraints
{style_rules}

## Context: Previously Published Posts
{prev_posts_str}

## Current Topic to Cover
- Title: {topic.title}
- Summary: {topic.summary}
- Source: {topic.source_name} ({topic.url})

## Objective
Write an insightful, professional, and technical post analyzing this topic from your perspective as {persona.name}.

## Required Output Schema
You MUST return ONLY a raw valid JSON object (no markdown codeblock markers, no surrounding text) with the following structure:
{{
  "text": "The main technical commentary/post body written in your voice (2-4 concise, impactful paragraphs).",
  "rationale": "A structured explanation covering: 1) Why this topic was selected, 2) Why it is relevant now, 3) Why it was chosen over alternative topics.",
  "sources": [
    "{topic.url}"
  ]
}}
"""
        return prompt.strip()
