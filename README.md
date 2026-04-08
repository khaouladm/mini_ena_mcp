# 🧬 Mini ENA MCP Server 

A minimal **Model Context Protocol (MCP)** server that exposes a subset of the **European Nucleotide Archive (ENA) REST API** as structured, schema-validated tools for AI agents.

This project is a **prototype implementation** inspired by a larger goal: enabling LLM-based systems to interact with biological data sources **reliably and deterministically**, without hallucination.

---

## 🚀 Features

- 🔧 MCP tools with **schema-first design (Pydantic)**
- 🌐 Real-time integration with **ENA Portal API**
- ⚡ Async HTTP client using `httpx`
- 🧠 Deterministic responses (no ambiguity, no hallucination)
- 🧩 Modular structure (easy to extend into full MCP server)

---

## 🛠️ Available Tools

### 1. `resolve_accession(accession)`
Detects the type of an ENA accession using deterministic prefix rules.

**Example:**
```json
Input:  "PRJEB12345"
Output: {
  "accession": "PRJEB12345",
  "record_type": "study",
  "explanation": "This looks like a study/project accession."
}
```

### 2. `ena_get_study(accession)`

Fetches study metadata from the ENA Portal API.

**Returns:**
- Study accession
- Title & description
- Taxonomy info
- Center name
- Publication date

### 3. `ena_get_taxonomy(query)`

Searches ENA taxonomy by scientific or common name.

**Example:**
```json
Input: "Homo sapiens"
Output: {
  "query": "Homo sapiens",
  "scientific_name": "Homo sapiens",
  "taxonomy_id": 9606,
  "common_name": "human"
}
```

---

## 🧠 Why MCP?

Traditional REST APIs are not designed for LLMs.

LLMs tend to:
- Hallucinate endpoints
- Invent parameters
- Misinterpret responses

👉 **MCP solves this by:**
- Enforcing input/output schemas
- Providing structured, validated tools
- Enabling deterministic interactions

---

## 🏗️ Architecture Overview

This mini version follows a simplified layered design:

```
MCP Server (FastMCP)
        ↓
Tool Layer (functions)
        ↓
Validation Layer (Pydantic)
        ↓
ENA Client Layer (httpx)
        ↓
ENA REST API
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/mini-ena-mcp-v2.git
cd mini-ena-mcp-v2

pip install -r requirements.txt
```

---

## ▶️ Running the Server

```bash
python app.py
```

---

## 🧪 Example Use Cases

- Identify accession types programmatically
- Retrieve structured ENA study metadata
- Query taxonomy information for organisms
- Build AI agents that interact with biological datasets safely

---

## ⚠️ Error Handling

The server returns structured error responses such as:

```json
{
  "error": "STUDY_NOT_FOUND",
  "message": "No ENA study found for accession: PRJEBXXXX"
}
```

---

## 📈 Future Improvements (Towards Full MCP)

- 🧩 Add more ENA endpoints (sample, run, experiment)
- 🔗 Composite tools (study → sample → run)
- ⚡ Caching layer (TTL-based)
- 🚦 Rate limiting & retry logic
- 🐳 Docker support
- 🔁 CI/CD pipeline (GitHub Actions)
- 📚 Full documentation site (MkDocs)

---

## 🎯 Project Goal

This project is a stepping stone toward building a production-grade MCP server for ENA, enabling:

- AI-driven bioinformatics workflows
- Reliable data access for LLM agents
- Reduced hallucination in scientific queries



