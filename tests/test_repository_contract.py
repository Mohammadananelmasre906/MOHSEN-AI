from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_privacy_policy_is_empty():
    policy = ROOT / "سياسة الخصوصية.txt"
    assert policy.exists()
    assert policy.read_bytes() == b""


def test_core_and_admin_are_separate_apps():
    assert (ROOT / "apps/mohsen-core/mohsen_core/main.py").is_file()
    assert (ROOT / "apps/mohsen-admin/mohsen_admin/main.py").is_file()


def test_no_pretrained_weights_are_bundled():
    forbidden = (".pt", ".pth", ".safetensors", ".gguf")
    assert not [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in forbidden]
