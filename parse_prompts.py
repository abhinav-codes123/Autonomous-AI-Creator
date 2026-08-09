import json

transcript_path = "/Users/mac/.gemini/antigravity/brain/3f04ef3a-7529-4e72-8e05-e42cb1f45dd4/.system_generated/logs/transcript.jsonl"
prompts = []

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                content = data.get('content', '')
                if '<USER_REQUEST>' in content:
                    start = content.find('<USER_REQUEST>') + len('<USER_REQUEST>')
                    end = content.find('</USER_REQUEST>')
                    prompt = content[start:end].strip()
                    prompts.append(prompt)
        except Exception as e:
            pass

with open('PROMPTS.md', 'w') as f:
    f.write('# User Prompts\n\n')
    for i, prompt in enumerate(prompts, 1):
        f.write(f"## Prompt {i}\n{prompt}\n\n")

print(f"Extracted {len(prompts)} prompts.")
