import json, csv, re, os
from datetime import datetime
import pandas as pd

INPUT = 'testdata.xlsx'
os.makedirs('reports', exist_ok=True)

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

def valid_date(s):
    try:
        datetime.strptime(str(s), '%Y-%m-%d'); return True
    except Exception:
        return False

def validate_row(r):
    errs = []
    if not str(r.get('name','')).strip(): errs.append('Name required')
    if not EMAIL_RE.match(str(r.get('email','')).strip()): errs.append('Invalid email')
    if not valid_date(r.get('date')): errs.append('Invalid date YYYY-MM-DD')
    try:
        if float(r.get('amount')) < 0: errs.append('Invalid amount (>=0)')
    except Exception:
        errs.append('Invalid amount (>=0)')
    return errs

def main():
    df = pd.read_excel(INPUT)
    payloads, audits = [], []
    for _, row in df.iterrows():
        d = dict(row); errs = validate_row(d); status = 'PASS' if not errs else 'FAIL'
        payloads.append({**d, 'status': status, 'errors': errs})
        audits.append({'case_id': d.get('case_id'), 'status': status,
                       'error_count': len(errs), 'errors_joined': '; '.join(errs)})
    with open('reports/validated_payloads.json','w',encoding='utf-8') as f: json.dump(payloads, f, indent=2, ensure_ascii=False)
    with open('reports/audit.csv','w',encoding='utf-8',newline='') as f:
        w = csv.DictWriter(f, fieldnames=['case_id','status','error_count','errors_joined']); w.writeheader(); w.writerows(audits)
    print('OK: /reports/validated_payloads.json, /reports/audit.csv')

if __name__ == '__main__':
    main()
