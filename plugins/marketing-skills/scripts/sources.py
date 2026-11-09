#!/usr/bin/env python3
"""Per-skill provenance: write SOURCES.md for single-source skills and check every skill's table.

Usage:
  python3 scripts/sources.py generate <skill> <corey|ali> <upstream-skill-path> --sources DIR [--note TEXT]
  python3 scripts/sources.py check [--sources DIR]

DIR holds the upstream snapshots: DIR/corey (repo root) and DIR/alirezarezvani (the marketing-skill/
folder). `generate` compares each section and file of the skill with the upstream copy and marks it
`as is` or `edited`. `check` verifies that every SKILL.md section and every file has a row, and, with
--sources, that each `as is` row really matches upstream. Stdlib only; writes only <skill>/SOURCES.md.
"""
import argparse
import filecmp
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKILLS = os.path.join(ROOT, 'skills')
COMMITS = {'corey': '96798cf', 'ali': '8f08254'}
SNAP = {'corey': 'corey', 'ali': 'alirezarezvani'}
REPOS = ('corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · '
         'ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)')
DETAIL_DIRS = ('references', 'scripts', 'assets', 'evals')
GROUP_MIN = 6  # a sub-folder with at least this many files may be one row


def sections(path):
    """Return {'frontmatter': text, heading: text} for a SKILL.md, split at level-2 headings."""
    text = open(path, encoding='utf-8').read()
    out, current, buf = {}, None, []
    body = text
    if text.startswith('---\n'):
        end = text.find('\n---', 4)
        out['frontmatter'] = text[:end + 4]
        body = text[end + 4:]
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        if line.startswith('## ') and not fenced:
            if current is not None:
                out[current] = '\n'.join(buf).strip()
            current, buf = line[3:].strip(), [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = '\n'.join(buf).strip()
    return out


def detail_files(skill_dir):
    files = []
    for sub in DETAIL_DIRS:
        for base, _, names in os.walk(os.path.join(skill_dir, sub)):
            files += [os.path.relpath(os.path.join(base, n), skill_dir) for n in names
                      if not n.startswith('.') and n != '__pycache__' and not n.endswith('.pyc')]
    return sorted(files)


def generate(args):
    skill_dir = os.path.join(SKILLS, args.skill)
    up_dir = os.path.join(args.sources, SNAP[args.origin], args.upstream)
    tag = f'{args.origin} `{os.path.basename(args.upstream.rstrip("/"))}` @{COMMITS[args.origin]}'
    rows = []
    mine, theirs = sections(os.path.join(skill_dir, 'SKILL.md')), sections(os.path.join(up_dir, 'SKILL.md'))
    for name, text in mine.items():
        part = 'frontmatter' if name == 'frontmatter' else f'SKILL.md § {name}'
        if name == 'Sources and credits' or text.startswith('Sources and credits:'):
            continue
        if name in theirs:
            same = text == theirs[name]
            where = f'{args.upstream}/SKILL.md' + ('' if name == 'frontmatter' else f' § {name}')
            rows.append((part, tag, where, 'as is' if same else f'edited: {args.note or "central pass"}'))
        else:
            rows.append((part, 'merge', '—', f'new: {args.note or "added in the merge"}'))
    grouped = {}
    for rel in detail_files(skill_dir):
        top = rel.split(os.sep)[:2]
        key = os.sep.join(top) if len(top) == 2 and os.path.isdir(os.path.join(skill_dir, *top)) else None
        grouped.setdefault(key, []).append(rel)
    for key, files in sorted(grouped.items(), key=lambda kv: kv[0] or ''):
        if key and len(files) >= GROUP_MIN:
            diff = [f for f in files if not os.path.exists(os.path.join(up_dir, f))
                    or not filecmp.cmp(os.path.join(skill_dir, f), os.path.join(up_dir, f), shallow=False)]
            rows.append((f'{key}/ ({len(files)} files)', tag, f'{args.upstream}/{key}/',
                         'as is' if not diff else f'edited: {len(diff)} of {len(files)} files'))
            continue
        for rel in files:
            up = os.path.join(up_dir, rel)
            if not os.path.exists(up):
                rows.append((rel, 'merge', '—', f'new: {args.note or "added in the merge"}'))
            else:
                same = filecmp.cmp(os.path.join(skill_dir, rel), up, shallow=False)
                rows.append((rel, tag, f'{args.upstream}/{rel}', 'as is' if same else f'edited: {args.note or "central pass"}'))
    lines = [f'# Sources: {args.skill}', '', '| Part | From | Upstream file | Changed here |', '|---|---|---|---|']
    lines += [f'| {a} | {b} | {c} | {d} |' for a, b, c, d in rows]
    lines += ['', REPOS, '']
    open(os.path.join(skill_dir, 'SOURCES.md'), 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'{args.skill}: {len(rows)} rows')


def parse_table(path):
    rows = []
    for line in open(path, encoding='utf-8'):
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| Part '):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 4:
            rows.append(cells[:4])
    return rows


def check(args):
    problems, total = [], 0
    for skill in sorted(os.listdir(SKILLS)):
        skill_dir = os.path.join(SKILLS, skill)
        if not os.path.isdir(skill_dir):
            continue
        total += 1
        src = os.path.join(skill_dir, 'SOURCES.md')
        if not os.path.isfile(src):
            problems.append(f'{skill}: SOURCES.md missing')
            continue
        rows = parse_table(src)
        parts = [r[0] for r in rows]
        if 'Sources and credits: [SOURCES.md](SOURCES.md)' not in open(os.path.join(skill_dir, 'SKILL.md'), encoding='utf-8').read():
            problems.append(f'{skill}: SKILL.md lacks the SOURCES.md link line')
        for name in sections(os.path.join(skill_dir, 'SKILL.md')):
            label = 'frontmatter' if name == 'frontmatter' else f'SKILL.md § {name}'
            if not any(p == label or p.startswith(label + ' ') or p.startswith(label + ' (') for p in parts):
                problems.append(f'{skill}: no row for "{label}"')
        folder_rows = [p.split(' (')[0].rstrip('/') for p in parts if p.endswith('files)')]
        for rel in detail_files(skill_dir):
            if any(p == rel or p.startswith(rel + ' ') for p in parts) or any(rel.startswith(f + os.sep) for f in folder_rows):
                continue
            problems.append(f'{skill}: no row for file {rel}')
        for part, origin, upstream, changed in rows:
            if not changed.startswith(('as is', 'edited', 'new')):
                problems.append(f'{skill}: "{part}" has an unknown status "{changed}"')
            key = origin.split(' ')[0]
            if args.sources and changed.startswith('as is') and key in SNAP and upstream not in ('—', ''):
                up_path, _, heading = upstream.partition(' § ')
                up_full = os.path.join(args.sources, SNAP[key], up_path)
                if not os.path.exists(up_full):
                    problems.append(f'{skill}: "{part}" points to missing upstream {upstream}')
                elif heading and part.startswith('SKILL.md § '):
                    mine = sections(os.path.join(skill_dir, 'SKILL.md')).get(part[len('SKILL.md § '):])
                    if mine is not None and mine != sections(up_full).get(heading):
                        problems.append(f'{skill}: "{part}" says as is but differs from {upstream}')
                elif os.path.isfile(up_full) and os.path.isfile(os.path.join(skill_dir, part)):
                    if not filecmp.cmp(os.path.join(skill_dir, part), up_full, shallow=False):
                        problems.append(f'{skill}: "{part}" says as is but differs from {upstream}')
    print(f'skills: {total}  problems: {len(problems)}')
    for p in problems:
        print('PROBLEM', p)
    return 1 if problems else 0


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = parser.add_subparsers(dest='cmd', required=True)
g = sub.add_parser('generate')
g.add_argument('skill')
g.add_argument('origin', choices=list(COMMITS))
g.add_argument('upstream', help='path of the upstream skill inside the snapshot, e.g. skills/sms')
g.add_argument('--sources', required=True)
g.add_argument('--note', default='')
c = sub.add_parser('check')
c.add_argument('--sources', default='')
args = parser.parse_args()
sys.exit(generate(args) if args.cmd == 'generate' else check(args))
