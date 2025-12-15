import csv

def _find_field(fieldnames, keywords):
    if not fieldnames:
        return None
    for key in keywords:
        for fn in fieldnames:
            if key in fn.lower():
                return fn
    return None

def _to_float(val):
    if val is None:
        raise ValueError
    if isinstance(val, (int, float)):
        return float(val)
    s = val.strip().replace(',', '.')
    return float(s)

def calculer_moyennes(fichier_csv):
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fnames = reader.fieldnames or []
        cpu_field = _find_field(fnames, ['cpu'])
        mem_field = _find_field(fnames, ['mem', 'memory', 'mémoire', 'ram'])
        if cpu_field is None or mem_field is None:
            candidates = [fn for fn in fnames if not any(k in fn.lower() for k in ('time','date','timestamp','hor'))]
            if cpu_field is None and candidates:
                cpu_field = candidates[0]
            if mem_field is None and len(candidates) > 1:
                mem_field = candidates[1] if candidates[0] != cpu_field else candidates[1]
        cpu_vals = []
        mem_vals = []
        for row in reader:
            try:
                cpu_vals.append(_to_float(row.get(cpu_field)))
                mem_vals.append(_to_float(row.get(mem_field)))
            except Exception:
                continue
        def stats(vals):
            if not vals:
                return {'avg': None, 'min': None, 'max': None}
            return {'avg': sum(vals)/len(vals), 'min': min(vals), 'max': max(vals)}
        return {'cpu': stats(cpu_vals), 'memory': stats(mem_vals)}

def detecter_pics(fichier_csv, seuil_cpu, seuil_mem):
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fnames = reader.fieldnames or []
        cpu_field = _find_field(fnames, ['cpu'])
        mem_field = _find_field(fnames, ['mem', 'memory', 'mémoire', 'ram'])
        time_field = _find_field(fnames, ['time', 'timestamp', 'date', 'horodatage', 'horaire'])
        if cpu_field is None or mem_field is None:
            candidates = [fn for fn in fnames if not any(k in fn.lower() for k in ('time','date','timestamp','hor'))]
            if cpu_field is None and candidates:
                cpu_field = candidates[0]
            if mem_field is None and len(candidates) > 1:
                mem_field = candidates[1] if candidates[0] != cpu_field else candidates[1]
        pics = []
        for row in reader:
            try:
                cpu_v = _to_float(row.get(cpu_field))
                mem_v = _to_float(row.get(mem_field))
            except Exception:
                continue
            if cpu_v > float(seuil_cpu) or mem_v > float(seuil_mem):
                ts = row.get(time_field) if time_field else None
                pics.append({'timestamp': ts, 'cpu': cpu_v, 'memory': mem_v})
        return pics
