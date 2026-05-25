#!/usr/bin/env python3
"""
🧠 SPATIAL BRAIN ORGANIZER — Auto-layout & Knowledge Graph Manager

Cara pakai:
  python3 scripts/organize.py              # Auto-layout semua node
  python3 scripts/organize.py --add        # Tambah node baru interaktif
  python3 scripts/organize.py --graph      # Generate knowledge graph visual

Fungsi:
  • Membaca master.geojson
  • Memahami hubungan antar node (prerequisite, related, next)
  • Auto-assign koordinat: node berhubungan = berdekatan
  • Domain = komplek, hubungan = jalan, urutan = jalur belajar
"""

import json, os, math, sys
from collections import defaultdict, deque

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "master.geojson")

# ============================================================
# KONFIGURASI DISTRIK (Koordinat Pusat per Domain)
# ============================================================
DISTRICTS = {
    "knt":  {"center": [106.832, -6.178], "name": "Kawasan Perkantoran", "cols": 5, "spacing": 0.003},
    "klg":  {"center": [110.000, -4.000], "name": "Komplek Industri Energi", "cols": 4, "spacing": 2.5},
    "ofs":  {"center": [107.000, -5.800], "name": "Zona Lepas Pantai", "cols": 5, "spacing": 0.3},
    "dep":  {"center": [112.000, -5.000], "name": "Jaringan Distribusi", "cols": 10, "spacing": 3.0},
    "geo":  {"center": [109.000, -4.000], "name": "Kawasan Geothermal", "cols": 4, "spacing": 2.0},
    "ons":  {"center": [110.000, -3.000], "name": "Ladang Minyak Bumi", "cols": 5, "spacing": 2.0},
    "lng":  {"center": [116.000, -1.000], "name": "Terminal LNG", "cols": 3, "spacing": 3.0},
    "pgn":  {"center": [106.820, -6.190], "name": "Kantor PGN", "cols": 3, "spacing": 0.003},
    "ihc":  {"center": [108.000, -4.000], "name": "RS Pertamina", "cols": 4, "spacing": 2.0},
    "edu":  {"center": [106.838, -6.233], "name": "📚 KAWASAN PENDIDIKAN", "cols": 5, "spacing": 0.004},
    "edu-fisika": {"center": [106.838, -6.239], "name": "🏘️ Komplek Fisika", "cols": 4, "spacing": 0.004},
    "edu-coding": {"center": [106.838, -6.245], "name": "🏘️ Komplek Coding", "cols": 4, "spacing": 0.004},
}

# ============================================================
# BACA DATA
# ============================================================
def load_data():
    with open(DATA_PATH, "r") as f:
        return json.loads(f.read())

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================
# AUTO-LAYOUT ENGINE
# ============================================================
def build_graph(features):
    """Build knowledge graph: node_id -> {prerequisites, related, next}"""
    graph = {}
    index = {f["id"]: f for f in features if "id" in f}
    
    for f in features:
        fid = f.get("id")
        if not fid: continue
        props = f.get("properties", {})
        graph[fid] = {
            "id": fid,
            "title": props.get("title", ""),
            "category": props.get("category", ""),
            "domain": props.get("domain", props.get("category", "")),
            "difficulty": props.get("difficulty", 3),
            "prerequisites": [],
            "related": [],
            "next": [],
            "order": props.get("order", 0)
        }
        # Parse connections
        for conn in props.get("connections", []):
            target = conn.get("id", "")
            rel = conn.get("relation", "related")
            if rel == "prerequisite":
                graph[fid]["prerequisites"].append(target)
            elif rel == "next":
                graph[fid]["next"].append(target)
            else:
                graph[fid]["related"].append(target)
    
    return graph, index

def auto_layout(features, graph):
    """Auto-assign coordinates based on knowledge graph relationships"""
    # Group by domain/category
    domains = defaultdict(list)
    for f in features:
        fid = f.get("id", "")
        cat = f.get("properties", {}).get("category", "unknown")
        domains[cat].append(fid)
    
    for domain, node_ids in domains.items():
        # Determine which district config to use
        district_key = domain
        if district_key not in DISTRICTS:
            # Try sub-district
            for dk in DISTRICTS:
                if domain.startswith(dk):
                    district_key = dk
                    break
            else:
                continue
        
        cfg = DISTRICTS.get(district_key)
        if not cfg: continue
        
        cx, cy = cfg["center"]
        spacing = cfg["spacing"]
        cols = cfg["cols"]
        
        # Sort nodes by difficulty then by connections (prerequisites first)
        sorted_nodes = []
        remaining = set(node_ids)
        
        # Topological sort based on prerequisites
        visited = set()
        temp_visited = set()
        
        def visit(fid):
            if fid in visited: return
            if fid in temp_visited: return  # Circular dependency
            if fid not in remaining: return
            temp_visited.add(fid)
            g = graph.get(fid, {})
            for prereq in g.get("prerequisites", []):
                visit(prereq)
            temp_visited.discard(fid)
            visited.add(fid)
            sorted_nodes.append(fid)
        
        for fid in list(remaining):
            visit(fid)
        
        # Add any remaining nodes not in the graph
        for fid in remaining:
            if fid not in visited:
                sorted_nodes.append(fid)
        
        # Assign coordinates in a grid
        for i, fid in enumerate(sorted_nodes):
            row = i // cols
            col = i % cols
            x = cx + (col - cols/2) * spacing + (random_offset() * 0.3)
            y = cy + row * spacing * 0.6 + (random_offset() * 0.3)
            
            # Find feature and update coordinates
            for f in features:
                if f.get("id") == fid:
                    f["geometry"]["coordinates"] = [round(x, 6), round(y, 6)]
                    break
    
    return features

def random_offset():
    """Small random offset to avoid perfect grid alignment (more natural)"""
    import random
    return (random.random() - 0.5) * spacing * 0.5

# ============================================================
# ROUTE FINDER (Shortest Path in Knowledge Graph)
# ============================================================
def find_learning_path(graph, start_id, end_id):
    """Find shortest path from start to end in knowledge graph (BFS)"""
    if start_id not in graph or end_id not in graph:
        return None
    
    # BFS
    queue = deque([[start_id]])
    visited = {start_id}
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == end_id:
            return path
        
        g = graph[node]
        # Traverse: next, related, and any node that has this as prerequisite
        neighbors = list(g.get("next", [])) + list(g.get("related", []))
        
        # Also traverse reverse: find nodes that list this as prerequisite
        for nid, ng in graph.items():
            if node in ng.get("prerequisites", []) and nid not in visited:
                neighbors.append(nid)
        
        for neighbor in neighbors:
            if neighbor not in visited and neighbor in graph:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    
    return None

# ============================================================
# ADD NEW NODE (Interactive)
# ============================================================
def add_node(data, title, category, domain=None, prerequisites=None, 
             related=None, emoji="📌", tags=None, metadata=None, 
             youtube=None, difficulty=3):
    """Add a new knowledge node with auto-assigned position"""
    features = data["features"]
    # Generate ID
    cat_prefix = category[:3]
    existing = [f for f in features if f.get("id", "").startswith(cat_prefix)]
    nums = [int(f["id"].split("-")[1]) for f in existing if "-" in f.get("id","")]
    next_num = max(nums) + 1 if nums else 1
    fid = f"{cat_prefix}-{next_num:03d}"
    
    # Build connections
    connections = []
    if prerequisites:
        for p in prerequisites:
            connections.append({"id": p, "relation": "prerequisite", "label": f"→ Pelajari dulu"})
    if related:
        for r in related:
            connections.append({"id": r, "relation": "related", "label": "↔ Terkait"})
    
    node = {
        "id": fid,
        "type": "Feature",
        "properties": {
            "id": fid,
            "title": title,
            "emoji": emoji,
            "category": category,
            "tags": tags or [],
            "domain": domain or category,
            "description": "",
            "difficulty": difficulty,
            "accuracy": "medium",
            "metadata": metadata or {},
            "connections": connections,
            "media": {"youtube": [{"url": yt, "title": title}] if youtube else []},
            "style": {"marker_color": DISTRICTS.get(category, {}).get("color", "#888"), "marker_size": "medium"}
        },
        "geometry": {"type": "Point", "coordinates": [0, 0]}
    }
    
    features.append(node)
    print(f"  ✅ Node '{title}' ditambahkan dengan ID {fid}")
    return data

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    import random
    
    data = load_data()
    features = data["features"]
    graph, index = build_graph(features)
    
    if "--add" in sys.argv:
        # Interactive mode
        print("\n🧠 Tambah Node Baru")
        print("─" * 40)
        title = input("  Judul materi: ").strip()
        cat = input("  Kategori (edu/coding/fisika/dll): ").strip()
        emoji = input("  Emoji: ").strip() or "📌"
        yt = input("  YouTube URL (opsional): ").strip()
        prereq = input("  Prasyarat (ID pisah koma, opsional): ").strip().split(",") if input else []
        prereq = [p.strip() for p in prereq if p.strip()]
        
        data = add_node(data, title, cat, emoji=emoji, 
                       prerequisites=prereq, youtube=yt)
        
    elif "--graph" in sys.argv:
        # Print knowledge graph
        print("\n🧠 KNOWLEDGE GRAPH")
        print("─" * 80)
        for fid, g in sorted(graph.items()):
            prereqs = ", ".join(g["prerequisites"][:3])
            nexts = ", ".join(g["next"][:3])
            rels = ", ".join(g["related"][:3])
            print(f"  {g['title']:<30} | Prasyarat: {prereqs}")
            if nexts: print(f"  {'':<30} | Lanjutan: {nexts}")
    
    else:
        # Auto-layout mode
        print("\n🧠 Auto-layout semua node berdasarkan knowledge graph...")
        random.seed(42)  # Consistent layout
        spacing = 0.003  # Will be overridden per district
        
        for domain, cfg in DISTRICTS.items():
            cx, cy = cfg["center"]
            sp = cfg["spacing"]
            cols = cfg["cols"]
            
            # Filter features by category matching domain
            domain_features = []
            for f in features:
                cat = f.get("properties", {}).get("category", "")
                if cat == domain or (not domain.startswith("edu-") and cat == domain):
                    domain_features.append(f)
                elif domain.startswith("edu-") and cat == "edu":
                    # Check sub-domain
                    sub = domain.split("-", 1)[1]
                    tags = f.get("properties", {}).get("tags", [])
                    if sub in tags:
                        domain_features.append(f)
            
            # Sort by difficulty and connections
            sorted_fs = []
            for f in sorted(domain_features, key=lambda x: 
                           (x.get("properties",{}).get("difficulty", 3),
                            x.get("properties",{}).get("title", ""))):
                sorted_fs.append(f)
            
            # Grid layout
            for i, f in enumerate(sorted_fs):
                row = i // cols
                col = i % cols
                ox = (random.random() - 0.5) * sp * 0.3
                oy = (random.random() - 0.5) * sp * 0.3
                x = cx + (col - cols/2) * sp + (ox if sp > 0.01 else 0)
                y = cy + row * sp * 0.6 + (oy if sp > 0.01 else 0)
                f["geometry"]["coordinates"] = [round(x, 6), round(y, 6)]
        
        print(f"  ✅ {len(features)} node diatur posisinya")
    
    # Save
    save_data(data)
    print(f"  💾 Disimpan ke {DATA_PATH}")
