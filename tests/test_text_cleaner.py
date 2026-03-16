from src.text_cleaner import TextCleaner

def test_clean_removes_urls():
    raw = "hello https://example.com world"
    cleaner = TextCleaner(raw)
    out = cleaner.clean()
    assert "http" not in out

def test_clean_normalises_whitespace():
    raw = "hello     world\n\nthis   is   test"
    cleaner = TextCleaner(raw)
    out = cleaner.clean()
    assert out == "hello world this is test"
