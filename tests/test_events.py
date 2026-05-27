from unittest.mock import patch, MagicMock

from tamaterm.events import EventDetector, EventEffect


def test_event_effect_defaults():
    e = EventEffect()
    assert e.happiness == 0
    assert e.hunger == 0
    assert e.energy == 0
    assert e.hygiene == 0
    assert e.message == ""


def test_cpu_spike_fires_on_transition():
    det = EventDetector()
    with patch("tamaterm.events.HAS_PSUTIL", True), \
         patch("tamaterm.events.psutil") as mock_psutil:
        mock_psutil.cpu_percent.return_value = 90.0
        effect = det.detect_cpu_spike()
        assert effect is not None
        assert effect.energy == -5
        assert effect.happiness == -3
        assert "CPU spike" in effect.message

        # Should not fire again while still above threshold
        effect2 = det.detect_cpu_spike()
        assert effect2 is None


def test_cpu_spike_resets_when_below_threshold():
    det = EventDetector()
    with patch("tamaterm.events.HAS_PSUTIL", True), \
         patch("tamaterm.events.psutil") as mock_psutil:
        mock_psutil.cpu_percent.return_value = 90.0
        det.detect_cpu_spike()

        mock_psutil.cpu_percent.return_value = 50.0
        det.detect_cpu_spike()

        mock_psutil.cpu_percent.return_value = 85.0
        effect = det.detect_cpu_spike()
        assert effect is not None


def test_cpu_spike_no_psutil():
    det = EventDetector()
    with patch("tamaterm.events.HAS_PSUTIL", False):
        assert det.detect_cpu_spike() is None


def test_memory_pressure_fires_on_transition():
    det = EventDetector()
    mock_mem = MagicMock()
    mock_mem.percent = 95.0
    with patch("tamaterm.events.HAS_PSUTIL", True), \
         patch("tamaterm.events.psutil") as mock_psutil:
        mock_psutil.virtual_memory.return_value = mock_mem
        effect = det.detect_memory_pressure()
        assert effect is not None
        assert effect.happiness == -2
        assert effect.energy == -3
        assert "memory pressure" in effect.message

        # Should not fire again while still above threshold
        effect2 = det.detect_memory_pressure()
        assert effect2 is None


def test_memory_pressure_resets_when_below_threshold():
    det = EventDetector()
    mock_mem_high = MagicMock()
    mock_mem_high.percent = 95.0
    mock_mem_low = MagicMock()
    mock_mem_low.percent = 50.0
    with patch("tamaterm.events.HAS_PSUTIL", True), \
         patch("tamaterm.events.psutil") as mock_psutil:
        mock_psutil.virtual_memory.return_value = mock_mem_high
        det.detect_memory_pressure()

        mock_psutil.virtual_memory.return_value = mock_mem_low
        det.detect_memory_pressure()

        mock_psutil.virtual_memory.return_value = mock_mem_high
        effect = det.detect_memory_pressure()
        assert effect is not None


def test_memory_pressure_no_psutil():
    det = EventDetector()
    with patch("tamaterm.events.HAS_PSUTIL", False):
        assert det.detect_memory_pressure() is None


def test_git_activity_detects_new_commits():
    det = EventDetector()
    det._last_commit_count = 5
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "7"
        mock_sub.run.return_value = mock_result
        mock_sub.TimeoutExpired = TimeoutError

        effect = det.detect_git_activity()
        assert effect is not None
        assert effect.happiness == 16  # +8 * 2
        assert effect.energy == -6    # -3 * 2
        assert det._last_commit_count == 7


def test_git_activity_no_change():
    det = EventDetector()
    det._last_commit_count = 5
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "5"
        mock_sub.run.return_value = mock_result
        mock_sub.TimeoutExpired = TimeoutError

        effect = det.detect_git_activity()
        assert effect is None


def test_git_activity_initializes_count():
    det = EventDetector()
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "10"
        mock_sub.run.return_value = mock_result
        mock_sub.TimeoutExpired = TimeoutError

        effect = det.detect_git_activity()
        assert effect is None  # First call just initializes
        assert det._last_commit_count == 10


def test_git_activity_handles_timeout():
    det = EventDetector()
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_sub.run.side_effect = mock_sub.TimeoutExpired
        mock_sub.TimeoutExpired = TimeoutError
        effect = det.detect_git_activity()
        assert effect is None


def test_branch_change_detected():
    det = EventDetector()
    det._last_branch = "main"
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "feature"
        mock_sub.run.return_value = mock_result
        mock_sub.TimeoutExpired = TimeoutError

        effect = det.detect_branch_change()
        assert effect is not None
        assert effect.happiness == 5
        assert "main" in effect.message
        assert "feature" in effect.message


def test_branch_no_change():
    det = EventDetector()
    det._last_branch = "main"
    with patch("tamaterm.events.subprocess") as mock_sub:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "main"
        mock_sub.run.return_value = mock_result
        mock_sub.TimeoutExpired = TimeoutError

        effect = det.detect_branch_change()
        assert effect is None


def test_detect_all_aggregates():
    det = EventDetector()
    with patch.object(det, "detect_git_activity", return_value=EventEffect(happiness=8)), \
         patch.object(det, "detect_branch_change", return_value=None), \
         patch.object(det, "detect_cpu_spike", return_value=EventEffect(energy=-5)), \
         patch.object(det, "detect_memory_pressure", return_value=None):
        effects = det.detect_all()
        assert len(effects) == 2
