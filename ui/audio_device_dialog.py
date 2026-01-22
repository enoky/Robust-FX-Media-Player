from __future__ import annotations
from PySide6 import QtWidgets, QtCore, QtGui

class AudioDeviceSelectionDialog(QtWidgets.QDialog):
    def __init__(self, devices: list[dict], current_index: int | None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Audio Output Device")
        self.resize(600, 450)
        self._devices = devices
        self.selected_device_index = current_index
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Instruction label
        lbl = QtWidgets.QLabel("Select an audio output device:")
        layout.addWidget(lbl)
        
        # Filter Layout
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Filter by API:"))
        
        self.api_combo = QtWidgets.QComboBox()
        filter_layout.addWidget(self.api_combo, 1)
        layout.addLayout(filter_layout)
        
        # Tree Widget (used as a list with columns)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Device Name", "Channels"])
        self.tree.setColumnWidth(0, 400)
        self.tree.setColumnWidth(1, 80)
        self.tree.setAlternatingRowColors(True)
        self.tree.setRootIsDecorated(False) # Flat list look
        self.tree.setUniformRowHeights(True)
        layout.addWidget(self.tree)
        
        # Collect unique APIs
        self._apis = sorted(list(set(d['hostapi'] for d in devices)))
        self.api_combo.addItem("All APIs", None)
        for api in self._apis:
            self.api_combo.addItem(api, api)

        # Connect filter
        self.api_combo.currentIndexChanged.connect(self._refresh_list)

        # Initial selection logic
        initial_api = None
        if current_index is not None:
            # Find the device to determine its API
            for dev in devices:
                if dev['index'] == current_index:
                    initial_api = dev['hostapi']
                    break
        
        # Select API in combo
        if initial_api:
            index = self.api_combo.findData(initial_api)
            if index >= 0:
                self.api_combo.setCurrentIndex(index)
        
        self._refresh_list()

        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def _refresh_list(self):
        self.tree.clear()
        selected_api = self.api_combo.currentData()
        
        # Default Item (Always show asking "System Default")
        # Actually "Default" usually implies an API too (e.g. MME Default).
        # But we'll add a generic generic "Default" at the top if "All" is selected or no preference?
        # Let's add it always at the top.
        
        default_item = QtWidgets.QTreeWidgetItem(["Default System Device", "2"])
        default_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, None) # Index None
        font = default_item.font(0)
        font.setBold(True)
        default_item.setFont(0, font)
        self.tree.addTopLevelItem(default_item)
        
        # Filter devices
        filtered = []
        for dev in self._devices:
            if selected_api is None or dev['hostapi'] == selected_api:
                filtered.append(dev)
        
        for dev in filtered:
            name = dev['name']
            # If "All APIs", maybe append API name to disambiguate?
            if selected_api is None:
                name = f"{name} ({dev['hostapi']})"
                
            channels = str(dev['channels'])
            idx = dev['index']
            
            item = QtWidgets.QTreeWidgetItem([name, channels])
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, idx)
            self.tree.addTopLevelItem(item)
            
            if self.selected_device_index == idx:
                item.setSelected(True)
                self.tree.setCurrentItem(item)
                
        if self.selected_device_index is None:
            default_item.setSelected(True)
            self.tree.setCurrentItem(default_item)

    def _on_item_double_clicked(self, item, column):
        self.accept()

    def accept(self):
        item = self.tree.currentItem()
        if not item:
            return
        self.selected_device_index = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        super().accept()
