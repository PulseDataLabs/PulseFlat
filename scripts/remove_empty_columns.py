import csv
import glob
import os

data_dir = '/home/rodrigo/projects/PulseFlat/data'
exclude = {'consolidated.csv'}

csv_files = sorted(glob.glob(os.path.join(data_dir, '*.csv')))

for fpath in csv_files:
    fname = os.path.basename(fpath)
    if fname in exclude or fname.endswith('.bak'):
        continue

    with open(fpath, newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    if not rows:
        continue

    empty_counts = {h: 0 for h in headers}
    for row in rows:
        for h in headers:
            v = row.get(h, '')
            if not (v and v.strip()):
                empty_counts[h] += 1

    full_empty = [h for h in headers if empty_counts[h] == len(rows)]

    if not full_empty:
        continue

    new_headers = [h for h in headers if h not in full_empty]

    with open(fpath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        for row in rows:
            new_row = {k: v for k, v in row.items() if k in new_headers}
            writer.writerow(new_row)

    print(f'{fname}:')
    for h in full_empty:
        print(f'  removed column: {h}')
    print()
