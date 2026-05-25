# 🧠 Spatial Second Brain

**Sistem belajar dengan memori spasial.**
Setiap konsep, data, atau pengetahuan punya "alamat" di peta — karena otak manusia lebih mudah mengingat sesuatu secara spasial.

## 🚀 Cara Pakai

### Online (via GitHub Pages)
1. Upload folder ini ke GitHub
2. Settings → Pages → source: `main` / folder `brain-map`
3. Buka `https://[username].github.io/brain-map`

### Offline (lokal)
```bash
cd brain-map
python3 -m http.server 8000
# Buka http://localhost:8000
```

### File Explorer
Buka langsung `index.html` — tapi beberapa browser blokir fetch file lokal. Pakai http.server saja.

## 📁 Struktur Folder

```
brain-map/
├── index.html              ← Viewer utama (buka ini di browser)
├── data/
│   └── master.geojson      ← Semua data spasial (bisa dibuka langsung!)
├── README.md
└── scripts/
    └── server.py           ← Server lokal (python3 scripts/server.py)
```

## 📝 Cara Nambah Node Baru

### Opsi 1: Edit GeoJSON langsung
Buka `data/master.geojson`, tambah entry baru:

```json
{
  "id": "edu-008",
  "title": "Nama Konsep",
  "emoji": "📌",
  "category": "edu",
  "tags": ["tag1", "tag2"],
  "description": "Deskripsi singkat",
  "accuracy": "medium",
  "metadata": {
    "Key1": "Value1",
    "Key2": "Value2"
  },
  "media": {
    "youtube": [{"url": "https://youtu.be/xxx", "title": "Judul"}],
    "links": [{"url": "https://...", "title": "Link"}]
  },
  "connections": [
    {"id": "edu-001", "relation": "next", "label": "→ Lanjut ke ..."}
  ],
  "geometry": {
    "type": "Point",
    "coordinates": [106.830, -6.230]
  }
}
```

### Opsi 2: Via GitHub Web (tanpa coding)
1. Buka `data/master.geojson` di GitHub
2. Klik icon ✏️ (edit)
3. Copy-paste template di atas, ubah isinya
4. Commit → otomatis update web

## 🗺️ Sistem Grid Mind Palace

Untuk konsep abstrak (matematika, fisika, coding), pakai grid ini:

| Area | Koordinat | Topik |
|------|-----------|-------|
| **Kawasan Matematika** | 106.830-106.850, -6.230 | Kalkulus, Aljabar, Vektor |
| **Kawasan Fisika** | 106.830-106.850, -6.235 | Mekanika, Termodinamika |
| **Kawasan Coding** | 106.830-106.850, -6.240 | Python, Algoritma |
| **Kawasan Pemerintahan** | 106.800-106.860, -6.170 | Data Pemerintahan Indonesia |

Setiap "kawasan" ibarat distrik di kota. Jalan = hubungan antar konsep.

## 🎯 Fitur Viewer

| Fitur | Keterangan |
|-------|-----------|
| 🗺️ **Map** | Leaflet + OpenStreetMap, gratis tanpa API |
| 🔍 **Search** | Cari node berdasarkan judul atau tag |
| 🏷️ **Filter** | Per kategori (Kantor, Kilang, Pelajaran, dll) |
| 🌙 **Dark Mode** | Klik icon bulan/matahari |
| 📺 **Popup Kaya** | Tabel data, YouTube embed, link |
| 🔗 **Supply Chain** | Garis aliran (bisa toggle) |
| 📍 **Google Maps** | Klik kanan di peta → buka Google Maps lokasi itu |
| 📱 **Responsive** | Buka di HP, tablet, PC |

## 🏗️ Teknologi

- **Peta**: Leaflet.js + OpenStreetMap tiles (gratis, tanpa API key)
- **Data**: GeoJSON (format standar spasial, bisa dibaca langsung)
- **Hosting**: GitHub Pages (gratis)
- **Size**: ~42 KB GeoJSON + ~10 KB HTML = ringan

## 🧠 Filosofi

> "Kita ingat jalan pulang tanpa GPS — tapi lupa rumus yang baru dibaca 5 menit lalu.
> Karena otak kita punya **peta navigasi fisik** yang kuat, tapi **peta abstrak** yang lemah.
> Spatial Second Brain menjembatani keduanya."

— athalarieq, 2026
