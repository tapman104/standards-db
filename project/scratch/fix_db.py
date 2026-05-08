import sqlite3
import pathlib
import re
import yaml

DB_PATH = r"C:\Users\tapman\Desktop\std db exe\standard.db"
STANDARDS_ROOT = pathlib.Path(r"C:\Users\tapman\Desktop\standards db\project\domains\mechanical\fasteners")

def parse_markdown_table(text):
    lines = [l.strip() for l in text.strip().split('\n')]
    if len(lines) < 3: return []
    header_line = lines[0]
    headers = [h.strip().lower() for h in header_line.split('|') if h.strip()]
    data_rows = []
    for line in lines[2:]:
        if not line.strip() or '|' not in line: continue
        cells = [c.strip() for c in line.split('|')]
        if line.startswith('|'): cells = cells[1:]
        if line.endswith('|'): cells = cells[:-1]
        if len(cells) < len(headers): continue
        row_dict = {}
        for i, h in enumerate(headers):
            if i < len(cells): row_dict[h] = cells[i]
        data_rows.append(row_dict)
    return data_rows

def get_property_class_data(standard_name, content):
    match = re.search(r'# Mechanical Properties(.*?)(?=#|\Z)', content, re.DOTALL | re.IGNORECASE)
    if not match: return []
    section_content = match.group(1)
    table_match = re.search(r'(\|.*?\n\|[-| ]*?\n(?:\|.*?\n)+)', section_content)
    if not table_match: return []
    table_text = table_match.group(1)
    rows = parse_markdown_table(table_text)
    parsed_data = []
    for row in rows:
        pc = None; tensile = None; yield_val = None; proof = None; h_min = None; h_max = None
        for k, v in row.items():
            if 'class' in k:
                pc_match = re.search(r'(\d+\.\d+|\d+)', v)
                pc = pc_match.group(1) if pc_match else v
            elif 'tensile' in k or 'rm' in k:
                nums = re.findall(r'\d+', v)
                if nums: tensile = int(nums[0])
            elif 'yield' in k or 're' in k or 'rp0.2' in k:
                nums = re.findall(r'\d+', v)
                if nums: yield_val = int(nums[0])
            elif 'proof' in k:
                nums = re.findall(r'\d+', v)
                if nums: proof = int(nums[0])
            elif 'hardness' in k or 'hv' in k or 'hb' in k:
                v = v.replace('–', '-')
                parts = v.split('-')
                if len(parts) == 2: h_min = parts[0].strip(); h_max = parts[1].strip()
                elif len(parts) == 1: h_min = parts[0].strip()
        if pc:
            parsed_data.append({'standard': standard_name, 'property_class': pc, 'tensile_mpa': tensile, 'yield_mpa': yield_val, 'hardness_min': h_min, 'hardness_max': h_max, 'proof_load_mpa': proof})
    return parsed_data

def run_fix():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM mechanical_properties")
    md_files = list(STANDARDS_ROOT.rglob("*.md"))
    master_props = {}
    
    # 1. Direct parsing
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f: content = f.read()
        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match: continue
        try: fm = yaml.safe_load(fm_match.group(1))
        except: continue
        standard = fm.get('standard')
        if not standard: continue
        props = get_property_class_data(standard, content)
        for p in props:
            cur.execute("INSERT INTO mechanical_properties VALUES (?, ?, ?, ?, ?, ?, ?)", (p['standard'], p['property_class'], p['tensile_mpa'], p['yield_mpa'], p['hardness_min'], p['hardness_max'], p['proof_load_mpa']))
            if standard == 'GOST 1759.4-87': master_props[p['property_class']] = p

    # 2. Frontmatter fallback
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f: content = f.read()
        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match: continue
        try: fm = yaml.safe_load(fm_match.group(1))
        except: continue
        standard = fm.get('standard'); pcs = fm.get('property_classes')
        if standard and pcs and isinstance(pcs, list):
            cur.execute("SELECT COUNT(*) FROM mechanical_properties WHERE standard=?", (standard,))
            if cur.fetchone()[0] == 0:
                for pc in pcs:
                    pcm = re.search(r'(\d+\.\d+|\d+)', str(pc))
                    pc_clean = pcm.group(1) if pcm else str(pc)
                    if pc_clean in master_props:
                        p = master_props[pc_clean]
                        cur.execute("INSERT INTO mechanical_properties VALUES (?, ?, ?, ?, ?, ?, ?)", (standard, pc_clean, p['tensile_mpa'], p['yield_mpa'], p['hardness_min'], p['hardness_max'], p['proof_load_mpa']))

    # 3. Equivalents propagation (for those still empty like DIN 933)
    cur.execute("SELECT standard FROM standards")
    all_stds = [r[0] for r in cur.fetchall()]
    for std in all_stds:
        cur.execute("SELECT COUNT(*) FROM mechanical_properties WHERE standard=?", (std,))
        if cur.fetchone()[0] == 0:
            # Find an equivalent that HAS properties
            cur.execute("SELECT equivalent FROM equivalents WHERE standard=?", (std,))
            equivs = [r[0] for r in cur.fetchall()]
            for eq in equivs:
                if eq == std: continue
                cur.execute("SELECT property_class, tensile_mpa, yield_mpa, hardness_min, hardness_max, proof_load_mpa FROM mechanical_properties WHERE standard=?", (eq,))
                props = cur.fetchall()
                if props:
                    print(f"Propagating properties to {std} from {eq}")
                    for p in props:
                        cur.execute("INSERT INTO mechanical_properties VALUES (?, ?, ?, ?, ?, ?, ?)", (std, p[0], p[1], p[2], p[3], p[4], p[5]))
                    break

    # 4. Fix Equivalents self-references
    cur.execute("SELECT standard, body FROM standards")
    standards = cur.fetchall()
    for std_name, std_body in standards:
        cur.execute("SELECT COUNT(*) FROM equivalents WHERE standard=? AND body=?", (std_name, std_body))
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO equivalents (standard, body, equivalent) VALUES (?, ?, ?)", (std_name, std_body, std_name))

    conn.commit()
    conn.close()
    print("Fix complete.")

if __name__ == "__main__":
    run_fix()
