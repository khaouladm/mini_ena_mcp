from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from fastmcp import FastMCP
import httpx
import asyncio
mcp = FastMCP("mini-ena-mcp")

ENA_PORTAL_BASE = "https://www.ebi.ac.uk/ena/portal/api"
REQUEST_TIMEOUT = 20.0


class AccessionInput(BaseModel):
    accession: str = Field(..., min_length=3, description="ENA accession, e.g. PRJEB12345")


class AccessionOutput(BaseModel):
    accession: str
    record_type: Literal["study", "sample", "run", "experiment", "unknown"]
    explanation: str


class StudyOutput(BaseModel):
    accession: str
    title: Optional[str] = None
    description: Optional[str] = None
    taxon_id: Optional[str] = None
    scientific_name: Optional[str] = None
    center_name: Optional[str] = None
    first_public: Optional[str] = None
    raw: Optional[list[dict[str, Any]]] = None


class TaxonomyInput(BaseModel):
    query: str = Field(..., min_length=1, description="Scientific name or taxon query, e.g. Homo sapiens")


class TaxonomyOutput(BaseModel):
    query: str
    count: int
    results: list[dict[str, Any]]



def detect_accession_type(accession: str) -> tuple[str, str]:
    acc = accession.upper().strip()

    if acc.startswith("PRJ"):
        return "study", "This looks like a study/project accession."
    if acc.startswith(("ERS", "SRS")):
        return "sample", "This looks like a sample accession."
    if acc.startswith(("ERR", "SRR")):
        return "run", "This looks like a run accession."
    if acc.startswith(("ERX", "SRX")):
        return "experiment", "This looks like an experiment accession."

    return "unknown", "Prefix not recognized by this mini MCP."


async def ena_portal_get(params: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Generic helper for ENA Portal API.
    Returns parsed JSON rows.
    """
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(f"{ENA_PORTAL_BASE}/search", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool
def resolve_accession(accession: str) -> dict:
    """
    Resolve accession type using simple prefix heuristics.
    This is local deterministic logic.
    """
    validated = AccessionInput(accession=accession)
    record_type, explanation = detect_accession_type(validated.accession)

    return AccessionOutput(
        accession=validated.accession.upper().strip(),
        record_type=record_type,
        explanation=explanation
    ).model_dump()


@mcp.tool
async def ena_get_study(accession: str) -> dict:
    """
    Fetch study metadata from the ENA Portal API using a study accession.
    Example: PRJEBxxxx or PRJNAxxxx
    """
    validated = AccessionInput(accession=accession)
    acc = validated.accession.upper().strip()

    params = {
        "result": "study",
        "query": f'study_accession="{acc}"',
        "fields": ",".join([
            "study_accession",
            "study_title",
            "study_description",
            "tax_id",
            "scientific_name",
            "center_name",
            "first_public"
        ]),
        "format": "json",
    }

    try:
        rows = await ena_portal_get(params)
    except httpx.HTTPStatusError as exc:
        return {
            "error": "ENA_HTTP_ERROR",
            "status_code": exc.response.status_code,
            "message": str(exc)
        }
    except httpx.RequestError as exc:
        return {
            "error": "ENA_CONNECTION_ERROR",
            "message": str(exc)
        }

    if not rows:
        return {
            "error": "STUDY_NOT_FOUND",
            "message": f"No ENA study found for accession: {acc}"
        }

    row = rows[0]

    result = StudyOutput(
        accession=row.get("study_accession", acc),
        title=row.get("study_title"),
        description=row.get("study_description"),
        taxon_id=row.get("tax_id"),
        scientific_name=row.get("scientific_name"),
        center_name=row.get("center_name"),
        first_public=row.get("first_public"),
        raw=rows
    )

    return result.model_dump()


@mcp.tool
async def ena_get_taxonomy(query: str) -> dict:
    """
    Experimental taxonomy lookup placeholder.
    The ENA taxonomy query surface needs further endpoint-specific validation.
    """
    validated = TaxonomyInput(query=query)
    q = validated.query.strip()

    return {
        "query": q,
        "status": "not_implemented_yet",
        "message": (
            "Taxonomy lookup is temporarily disabled in this mini prototype. "
            "Study lookup works, but taxonomy requires a different ENA query path."
        )
    }


import asyncio

async def test():
    print("=== TEST resolve_accession ===")
    print(resolve_accession("PRJEB1001"))

    print("\n=== TEST ena_get_study ===")
    result = await ena_get_study("PRJEB1001")
    print(result)

if __name__ == "__main__":
    asyncio.run(test())