from pathlib import Path
D = "d" + "iv"
T = "MOTIONDIV"

def h(s):
    return s.replace(T, D)

p = Path(__file__).parent / "app.py"
t = p.read_text(encoding="utf-8")
t = t.replace(
    h("Year: <b>{edu.get('graduation_year', 'Not detected')}</b>\n            </MOTIONDIV>\n        </MOTIONDIV>"),
    h("Year: <b>{edu.get('graduation_year', 'Not detected')}</b>\n        </MOTIONDIV>"),
)
old = h("""        <MOTIONDIV style='background: var(--bg-muted); border-radius: 12px; padding: 16px;
                    border: 1px solid #E2E8F0;'>
            <MOTIONDIV style='color: var(--text-muted); font-size: 0.9rem; line-height: 2;'>
                Level: <b>{exp.get('estimated_level', 'Unknown')}</b><br>
                Years: <b>{exp.get('total_years', 0)} years estimated</b><br>
                Positions: <b>{len(exp.get('year_ranges', []))} detected</b><br>
            </MOTIONDIV>
        </MOTIONDIV>""")
new = h("""        <MOTIONDIV class='info-panel'>
                Level: <b>{exp.get('estimated_level', 'Unknown')}</b><br>
                Years: <b>{exp.get('total_years', 0)} years estimated</b><br>
                Positions: <b>{len(exp.get('year_ranges', []))} detected</b><br>
        </MOTIONDIV>""")
if old in t:
    t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("fixed")
