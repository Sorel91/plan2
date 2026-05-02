from g2p_modern.core.adapters import LegacySample
from g2p_modern.core.pipeline import GenerationPipeline
from g2p_modern.core.retrieval import BoundaryRetriever
from g2p_modern.core.schemas import Boundary, GenerateRequest, Point, RetrieveRequest


def test_pipeline_stub_returns_meta_status() -> None:
    pipeline = GenerationPipeline()
    request = GenerateRequest(boundary=Boundary(points=[Point(x=0, y=0), Point(x=1, y=0), Point(x=0, y=1)]))
    response = pipeline.generate(request)
    assert response.meta["status"] == "stub"


def test_retrieve_returns_sorted_candidates() -> None:
    retriever = BoundaryRetriever(
        [
            LegacySample(name="A", boundary=[(0, 0), (2, 0), (0, 2)], raw=None),
            LegacySample(name="B", boundary=[(100, 100), (102, 100), (100, 102)], raw=None),
        ]
    )
    result = retriever.retrieve(boundary=[(1, 1), (3, 1), (1, 3)], k=1)
    assert len(result) == 1
    assert result[0].name == "A"


def test_pipeline_retrieve_contract() -> None:
    pipeline = GenerationPipeline()
    payload = RetrieveRequest(boundary=Boundary(points=[Point(x=0, y=0), Point(x=1, y=0), Point(x=0, y=1)]), k=3)
    response = pipeline.retrieve(payload)
    assert response.meta["status"] == "ok"
