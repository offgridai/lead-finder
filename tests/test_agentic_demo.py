from pathlib import Path

from scripts.run_agentic_demo import run_demo


def test_agentic_demo_writes_storage_and_csv(tmp_path: Path):
    project_root = Path(__file__).resolve().parents[1]
    result = run_demo(project_root, tmp_path)

    assert result["raw_documents"] == 3
    assert result["candidates"] == 3
    assert result["leads"] == 3
    assert Path(result["csv_path"]).exists()
    assert Path(result["sqlite_path"]).exists()
