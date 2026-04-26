from g2p_modern.core.pipeline import GenerationPipeline
from g2p_modern.core.schemas import Boundary, GenerateRequest, Point


def test_pipeline_stub_returns_meta_status() -> None:
    pipeline = GenerationPipeline()
    request = GenerateRequest(boundary=Boundary(points=[Point(x=0, y=0), Point(x=1, y=0), Point(x=0, y=1)]))
    response = pipeline.generate(request)
    assert response.meta["status"] == "stub"
