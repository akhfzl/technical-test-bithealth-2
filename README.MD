# Technical Test — Modular FastAPI + LangGraph + Qdrant

Repository ini berisi implementasi backend berbasis **FastAPI**, **LangGraph**, dan **Qdrant**, dengan penerapan modularitas, konfigurasi environment, serta pengujian menggunakan **pytest**. Seluruh kode telah dirapikan dengan prinsip clean architecture dan keterpisahan komponen.

---

## 🚀 1. Environment & Installation

Project ini menggunakan:

- **Python v3.11.6**
- Dependency diatur melalui `requirements.txt`

### Instalasi

```bash
python3.11 -m venv myenv
source myenv/bin/activate       # Linux / Mac
myenv\Scripts\activate          # Windows

pip install -r requirements.txt
```

---

## 📁 2. Struktur Modular Project

Repository ini menerapkan struktur modular agar project mudah dirawat, diuji, dan diperluas.

```
app/
│
├── api/            # Routing FastAPI
├── services/       # Service layer (embedding, workflow, qdrant)
├── repositories/   # Data access abstraction layer
├── workflows/      # LangGraph workflow
├── schemas/        # Pydantic models
├── core/           # Dependency Injection, startup
└── config/         # Settings (.env)
```

Kelebihan pendekatan ini:

- Memisahkan business logic dari API
- Memudahkan unit testing
- Memudahkan dependency injection
- Mengurangi tight coupling antar komponen

---

## 🔐 3. Environment Variables (.env)

Credential dan konfigurasi tidak disimpan di kode melainkan pada file:

- `.env` (asli)
- `.env-example` (template yang aman untuk dishare)

Contoh `.env-example`:

```
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-api-key
QDRANT_COLLECTION=messy_documents
EMBED_DIM=384
```

Semua environment di-load otomatis melalui `pydantic-settings`.

---

## 🧩 4. Kendala & Temuan Teknis

Selama pengembangan, ditemukan berbagai masalah terkait integrasi:

### ◼ 4.1 API Qdrant Deprecation & Parameter Changes

Banyak method lama Qdrant yang **deprecated**, antara lain:

- `.search()` sudah tidak digunakan
- `.search` diganti menjadi `.query_points()`
- Parameter seperti `vector`, `query_vector`, `vectors`, `query_filter` sudah berubah format
- Pemanggilan Qdrant Cloud harus menggunakan `url=` bukan `host=` atau `port=`

Contoh yang benar:

```python
qdrant.query_points(
    collection_name="documents",
    query=[0.1, 0.2, 0.3],
    limit=5
)
```

### ◼ 4.2 Parameter Salah Sasaran

Beberapa error yang ditemukan:

- `"Unknown arguments: ['query_vector']"`
- `"Unknown arguments: ['vector']"`
- `"Unsupported query type: <class 'dict'>"`

Semua diselesaikan dengan menyesuaikan signature API Qdrant terbaru.

---

## 🧱 5. Penyesuaian Pydantic (v2.x)

Banyak model Pydantic perlu disesuaikan karena:

- `BaseSettings` pindah ke `pydantic-settings`
- `Union[...]` tidak boleh di-instansiasi sebagai tipe response
- Harus menggunakan `Optional[T]` atau `T | None`

Contoh model final:

```python
class WorkflowResult(BaseModel):
    initial_query: str
    retrieved_docs: List[DocumentSchema]
    final_answer: str
    processing_time: float
```

Model dibuat agar kompatibel dengan FastAPI + Pydantic v2.

---

## 🧪 6. Testing Menggunakan pytest

Pengujian dilakukan dengan **pytest**, mencakup:

### ✔ Unit Test

- Menguji workflow
- Menguji embedder
- Menguji Qdrant service dengan mock

### ✔ Integration Test

- Menguji endpoint FastAPI (`/query`, `/ingest`) menggunakan TestClient
- Menggunakan dependency override agar tidak perlu koneksi Qdrant

### Menjalankan test:

```bash
pytest -v
```

Struktur test:

```
tests/
│
├── unit/
├── integration/
└── conftest.py
```

Dengan mocking, semua test dapat dijalankan **tanpa koneksi internet** dan **tanpa Qdrant Cloud**.

---

## 📌 Ringkasan

| Fitur                                           | Status    |
| ----------------------------------------------- | --------- |
| Modularisasi project                            | ✔ Selesai |
| Environment config (.env)                       | ✔ Selesai |
| Penyesuaian Pydantic v2                         | ✔ Selesai |
| Perbaikan Qdrant API terbaru                    | ✔ Selesai |
| Unit test + Integration test menggunakan pytest | ✔ Selesai |
| Mocking dependencies                            | ✔ Selesai |

---

## 🎉 Penutup

Project ini memperlihatkan implementasi arsitektur Python modern yang scalable, testable, dan production-ready.
Fokus utama mencakup modularitas, pemisahan service layer, integrasi ke Qdrant, workflow AI (LangGraph), dan testability.

Silakan gunakan, modifikasi, dan kembangkan sesuai kebutuhan.
