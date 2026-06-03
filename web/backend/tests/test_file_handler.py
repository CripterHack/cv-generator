import pytest
import os
import base64
from unittest.mock import patch
from PIL import Image
from io import BytesIO

from shared.utils.file_handler import FileHandler


def _make_image_base64(width=100, height=100, fmt="PNG"):
    img = Image.new("RGB", (width, height), color="red")
    buf = BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@pytest.fixture
def upload_dir(tmp_path):
    upload_path = tmp_path / "uploads"
    upload_path.mkdir()
    return upload_path


class TestSavePhoto:
    def test_save_valid_photo(self, upload_dir):
        with patch("shared.utils.file_handler.UPLOAD_DIR", str(upload_dir)):
            b64 = _make_image_base64()
            result = FileHandler.save_photo(b64, "test.png")
            assert result is not None
            assert os.path.exists(result)
            assert "test.png" in result

    def test_save_photo_with_data_uri_prefix(self, upload_dir):
        with patch("shared.utils.file_handler.UPLOAD_DIR", str(upload_dir)):
            b64 = _make_image_base64()
            data_uri = f"data:image/png;base64,{b64}"
            result = FileHandler.save_photo(data_uri, "prefixed.png")
            assert result is not None
            assert os.path.exists(result)

    def test_save_photo_resizes_large_image(self, upload_dir):
        with patch("shared.utils.file_handler.UPLOAD_DIR", str(upload_dir)):
            b64 = _make_image_base64(width=2000, height=2000)
            result = FileHandler.save_photo(b64, "large.png")
            assert result is not None
            saved = Image.open(result)
            assert max(saved.size) <= 800

    def test_save_photo_returns_none_on_invalid_base64(self, upload_dir):
        with patch("shared.utils.file_handler.UPLOAD_DIR", str(upload_dir)):
            result = FileHandler.save_photo("not-valid-base64!!!", "bad.png")
            assert result is None

    def test_save_photo_rejects_oversized_file(self, upload_dir):
        with patch("shared.utils.file_handler.UPLOAD_DIR", str(upload_dir)):
            with patch("shared.utils.file_handler.MAX_UPLOAD_SIZE", 10):
                b64 = _make_image_base64(width=200, height=200)
                result = FileHandler.save_photo(b64, "oversized.png")
                assert result is None


class TestLoadPhoto:
    def test_load_existing_photo(self, upload_dir):
        b64 = _make_image_base64()
        img_data = base64.b64decode(b64)
        file_path = upload_dir / "load_test.png"
        file_path.write_bytes(img_data)

        result = FileHandler.load_photo(str(file_path))
        assert result is not None
        assert result.startswith("data:image/png;base64,")

    def test_load_nonexistent_photo(self):
        result = FileHandler.load_photo("/nonexistent/path/photo.png")
        assert result is None


class TestDeletePhoto:
    def test_delete_existing_photo(self, upload_dir):
        file_path = upload_dir / "delete_test.png"
        file_path.write_bytes(b"fake image data")
        assert file_path.exists()

        result = FileHandler.delete_photo(str(file_path))
        assert result is True
        assert not file_path.exists()

    def test_delete_nonexistent_photo(self):
        result = FileHandler.delete_photo("/nonexistent/path/photo.png")
        assert result is False
