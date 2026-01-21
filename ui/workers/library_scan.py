import os
from PySide6 import QtCore
from library import LibraryService
from metadata import probe_metadata

VIDEO_EXTS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".webm",
    ".avi",
}

class LibraryScanWorker(QtCore.QThread):
    progress = QtCore.Signal(int, str)
    finished = QtCore.Signal(int)
    preliminary_finished = QtCore.Signal()  # Emitted when first batch is ready

    def __init__(self, library: LibraryService, paths: list[str], is_folder: bool, parent=None):
        super().__init__(parent)
        self.library = library
        self.paths = paths
        self._is_folder = is_folder
        self._abort = False

    def run(self):
        count = 0
        
        # 1. Fast Scan Phase:
        # Collect all files first
        all_files = []
        if self._is_folder:
            for folder_path in self.paths:
                if self._abort:
                    break
                for root, _, files in os.walk(folder_path):
                    if self._abort:
                        break
                    for f in files:
                        _, ext = os.path.splitext(f)
                        # TODO: Import MEDIA_EXTS constant or redefine
                        # For now, let's assume we can pass it or duplicate logic. 
                        # Actually probe_metadata handles extension checks usually or we rely on main window.
                        # Let's import MEDIA_EXTS if possible or duplicate.
                        # Duplicating for now to match logic seen in outline/assumed
                        if ext.lower() in {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".mp4", ".mkv", ".mov", ".webm", ".avi"}:
                             all_files.append(os.path.join(root, f))
        else:
            all_files = self.paths

        total_files = len(all_files)
        
        # 2. Metadata Extraction Phase
        batch: list = []
        
        def fast_meta_extractor(path: str):
            # Probe local metadata ONLY (fast)
            # online fetch is skipped here for speed, or maybe we want it?
            # Original code likely called probe_metadata(path) which defaults to fetch_online=True
            # But inside a worker we might want to be careful.
            # Let's check what the original code did. 
            # Original code: meta = probe_metadata(path)
            # We will use the same.
            return probe_metadata(path)

        def progress_wrapper(count: int, path: str):
             self._emit_progress(count, f"scanning: {os.path.basename(path)}")
        
        # We can process sequentially or thread pool. 
        # Since this IS a thread, we can just loop. 
        # Original code seemed to use a thread pool inside?
        # Let's stick to what was likely there or a simple loop if not visible.
        # Wait, I should double check imports I need. 
        # I imported probe_metadata.
        
        for i, path in enumerate(all_files):
            if self._abort:
                break
                
            try:
                # Synchronous probe for now to avoid complexity of nested threads if not needed
                # But wait, looking at the previous view_file_outline, LibraryScanWorker had:
                # full_meta_extractor, fast_meta_extractor using concurrent.futures?
                # I should probably have copied the EXACT code from view_code_item. 
                # The view_code_item output below will give me the exact content.
                # I will paste THAT.
                pass
            except Exception:
                pass

        # ... (This file content is a placeholder, I will overwrite it with the ACTUAL content from the previous tool output)
