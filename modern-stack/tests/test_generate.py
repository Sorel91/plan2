from g2p_modern.core.pipeline import GenerateRequest, GenerationPipeline


def test_generate_creates_rooms_and_generated_status():
    pipeline = GenerationPipeline()
    request = GenerateRequest(
        boundary=[[0, 0], [10, 0], [10, 8], [0, 8]],
        constraints=[
            {"room_type": "living", "min_count": 1},
            {"room_type": "kitchen", "min_count": 1},
            {"room_type": "bedroom", "min_count": 2},
            {"room_type": "bathroom", "min_count": 1},
        ],
    )

    response = pipeline.generate(request)

    assert response.rooms
    assert response.meta["status"] != "stub"
    assert response.meta["status"] == "generated"
