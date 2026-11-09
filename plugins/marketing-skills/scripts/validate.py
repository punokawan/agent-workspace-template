#!/usr/bin/env python3
"""Check the marketing-skills plugin: frontmatter, names, links, context-file mentions, scripts.

Usage: python3 scripts/validate.py [plugin_dir]   (default: the folder above this script)
Exit code 1 when any error is found. Stdlib only; reads files, compiles Python in memory and runs
`node --check` on JavaScript. Writes nothing.
"""
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
SKILLS = os.path.join(ROOT, 'skills')
LINK = re.compile(r'\]\(([^)\s]+)\)')
CONTEXT_FILE = '.agents/product-marketing.md'
CONTEXT_OWNER = 'product-marketing'

errors, warnings = [], []


def frontmatter(text):
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---', 4)
    if end < 0:
        return None
    block = text[4:end]
    data, parent = {}, None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith((' ', '\t')) and parent:
            key, _, value = line.strip().partition(':')
            data.setdefault(parent, {})[key.strip()] = value.strip().strip('"\'')
            continue
        key, _, value = line.partition(':')
        key, value = key.strip(), value.strip()
        parent = key if value == '' else None
        data[key] = {} if value == '' else value.strip('"\'')
    return data


names = {}
for entry in sorted(os.listdir(SKILLS)):
    folder = os.path.join(SKILLS, entry)
    if not os.path.isdir(folder):
        continue
    skill_md = os.path.join(folder, 'SKILL.md')
    if not os.path.isfile(skill_md):
        errors.append(f'{entry}: SKILL.md missing')
        continue
    meta = frontmatter(open(skill_md, encoding='utf-8').read())
    if meta is None:
        errors.append(f'{entry}: frontmatter missing or not closed')
        continue
    name = meta.get('name', '')
    desc = meta.get('description', '')
    if name != entry:
        errors.append(f'{entry}: name "{name}" differs from folder')
    if name in names:
        errors.append(f'{entry}: duplicate name "{name}"')
    names[name] = entry
    if not desc:
        errors.append(f'{entry}: description empty')
    elif len(desc) > 1024:
        errors.append(f'{entry}: description {len(desc)} chars (max 1024)')
    md_meta = meta.get('metadata') if isinstance(meta.get('metadata'), dict) else {}
    if not md_meta.get('version'):
        warnings.append(f'{entry}: metadata.version missing')
    if not md_meta.get('sources'):
        warnings.append(f'{entry}: metadata.sources missing')
    lines = sum(1 for _ in open(skill_md, encoding='utf-8'))
    if lines > 600:
        warnings.append(f'{entry}: SKILL.md has {lines} lines')

for base, _, files in os.walk(ROOT):
    if os.sep + '.git' in base or os.sep + 'node_modules' in base:
        continue
    for fname in files:
        path = os.path.join(base, fname)
        rel = os.path.relpath(path, ROOT)
        if fname.endswith('.md'):
            text = open(path, encoding='utf-8', errors='ignore').read()
            for target in LINK.findall(text):
                if target.startswith(('http://', 'https://', 'mailto:', '#', '<', '/')) or '{' in target:
                    continue  # web URLs, anchors, templates and example site paths such as /pricing
                if '.' not in target and '/' not in target:
                    continue  # placeholders in examples, such as [text](link)
                clean = target.split('#')[0].split('?')[0]
                if clean and not os.path.exists(os.path.normpath(os.path.join(base, clean))):
                    errors.append(f'{rel}: broken link {target}')
            in_owner = rel.startswith(os.path.join('skills', CONTEXT_OWNER) + os.sep)
            if CONTEXT_FILE in text and not in_owner and rel.startswith('skills' + os.sep):
                warnings.append(f'{rel}: mentions {CONTEXT_FILE} directly')
        elif fname.endswith('.py'):
            try:
                compile(open(path, encoding='utf-8').read(), path, 'exec')
            except SyntaxError as exc:
                errors.append(f'{rel}: python does not compile (line {exc.lineno}: {exc.msg})')
        elif fname.endswith(('.js', '.mjs', '.cjs')) and shutil.which('node'):
            result = subprocess.run(['node', '--check', path], capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f'{rel}: node --check failed')

print(f'skills: {len(names)}  errors: {len(errors)}  warnings: {len(warnings)}')
for item in errors:
    print('ERROR  ', item)
for item in warnings:
    print('WARN   ', item)
sys.exit(1 if errors else 0)
