"""第5回 宿題（実装）: 前後ページを足す処理のテスト（APIキーを使わない）。"""

from app.retrieval import add_neighbors, load_pages


def hit(pages, page_id, distance=0.1):
    page = next(p for p in pages if p["page_id"] == page_id)
    return {**page, "distance": distance}


def ids(results):
    return [r["page_id"] for r in results]


def test_window_zero_returns_hits_unchanged():
    pages = load_pages()
    hits = [hit(pages, pages[10]["page_id"])]
    assert add_neighbors(hits, pages, 0) == hits


def test_adds_previous_and_next_page():
    pages = load_pages()
    hits = [hit(pages, pages[10]["page_id"])]
    results = add_neighbors(hits, pages, 1)
    assert ids(results) == [pages[10]["page_id"], pages[9]["page_id"], pages[11]["page_id"]]
    assert results[1]["neighbor_of"] == pages[10]["page_id"]
    assert "distance" not in results[1]


def test_does_not_cross_documents():
    pages = load_pages()
    last = max(i for i, p in enumerate(pages) if p["document_id"] == pages[0]["document_id"])
    results = add_neighbors([hit(pages, pages[last]["page_id"])], pages, 1)
    assert {r["document_id"] for r in results} == {pages[last]["document_id"]}
    assert len(results) == 2  # 前のページだけ


def test_no_duplicates_and_hits_keep_distance():
    pages = load_pages()
    # 隣り合う2ページが両方とも検索で当たった場合
    hits = [hit(pages, pages[20]["page_id"], 0.1), hit(pages, pages[21]["page_id"], 0.2)]
    results = add_neighbors(hits, pages, 1)
    assert len(ids(results)) == len(set(ids(results)))
    assert ids(results) == [pages[20]["page_id"], pages[19]["page_id"],
                            pages[21]["page_id"], pages[22]["page_id"]]
    assert results[2]["distance"] == 0.2
