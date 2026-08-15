import sqlite3
conn = sqlite3.connect('data/data.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute('PRAGMA table_info(jobs)')
cols = [r[1] for r in cur.fetchall()]
print('Job columns:', cols)
cur.execute('SELECT * FROM jobs LIMIT 1')
row = cur.fetchone()
if row:
    print('Row dict:', dict(row))
else:
    print('No jobs')
cur.execute('SELECT status, completed_at FROM jobs')
for r in cur.fetchall():
    print('Status:', r['status'], 'completed_at:', repr(r['completed_at']))
conn.close()
