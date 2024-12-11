import sys

import fitz  # PyMuPDF
from PyQt5.QtCore import QPoint, QSettings, Qt
from PyQt5.QtGui import QCursor, QDoubleValidator, QImage, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QShortcut,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class DraggableLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.last_pos = None
        self.setCursor(Qt.OpenHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.last_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            self.last_pos = None

    def mouseMoveEvent(self, event):
        if self.last_pos is not None:
            delta = event.pos() - self.last_pos

            # Get the scroll area
            scroll_area = self.parent().parent()

            # Update scroll bars
            hbar = scroll_area.horizontalScrollBar()
            vbar = scroll_area.verticalScrollBar()

            hbar.setValue(hbar.value() - delta.x())
            vbar.setValue(vbar.value() - delta.y())

            self.last_pos = event.pos()


class PDFReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced PDF Reader")
        self.setGeometry(100, 100, 1000, 800)

        # Initialize settings
        self.settings = QSettings("PDFReader", "ZoomHistory")
        self.zoom_history = self.settings.value("zoom_history", [], type=list)

        # Create stacked widget to handle normal and fullscreen views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create normal view widget
        self.normal_widget = QWidget()
        self.normal_layout = QVBoxLayout()
        self.normal_widget.setLayout(self.normal_layout)

        # Create fullscreen view widget
        self.fullscreen_widget = QWidget()
        self.fullscreen_layout = QVBoxLayout()
        self.fullscreen_widget.setLayout(self.fullscreen_layout)

        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.normal_widget)
        self.stacked_widget.addWidget(self.fullscreen_widget)

        # Zoom controls
        zoom_layout = QHBoxLayout()
        zoom_in_btn = QPushButton("Zoom In +0.1 (Ctrl++)")
        zoom_out_btn = QPushButton("Zoom Out -0.1 (Ctrl+-)")
        open_pdf_btn = QPushButton("Open PDF")

        # Add rotation buttons
        rotate_90_btn = QPushButton("Rotate 90° (Ctrl+R)")
        rotate_neg_90_btn = QPushButton("Rotate -90° (Ctrl+Shift+R)")

        # Add full screen button
        fullscreen_btn = QPushButton("Full Screen (Ctrl+F)")

        zoom_layout.addWidget(open_pdf_btn)
        zoom_layout.addWidget(zoom_in_btn)
        zoom_layout.addWidget(zoom_out_btn)
        zoom_layout.addWidget(rotate_90_btn)
        zoom_layout.addWidget(rotate_neg_90_btn)
        zoom_layout.addWidget(fullscreen_btn)
        self.normal_layout.addLayout(zoom_layout)

        # Create PDF display widgets
        self.normal_image_label = DraggableLabel()
        self.normal_image_label.setAlignment(Qt.AlignCenter)
        self.fullscreen_image_label = DraggableLabel()
        self.fullscreen_image_label.setAlignment(Qt.AlignCenter)

        # Create scroll areas for both normal and fullscreen views
        self.normal_scroll_area = QScrollArea()
        self.normal_scroll_area.setWidget(self.normal_image_label)
        self.normal_scroll_area.setWidgetResizable(True)
        # Hide scrollbars but keep functionality
        self.normal_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.normal_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.normal_layout.addWidget(self.normal_scroll_area)

        self.fullscreen_scroll_area = QScrollArea()
        self.fullscreen_scroll_area.setWidget(self.fullscreen_image_label)
        self.fullscreen_scroll_area.setWidgetResizable(True)
        # Hide scrollbars but keep functionality
        self.fullscreen_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fullscreen_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.fullscreen_layout.addWidget(self.fullscreen_scroll_area)

        # Current document and zoom level
        self.current_doc = None
        self.current_page = None
        self.zoom_level = 1.0
        self.rotation = 0
        self.is_fullscreen = False
        self.is_inverted = False  # Track inversion state

        # Connect buttons
        open_pdf_btn.clicked.connect(self.open_pdf)
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn.clicked.connect(self.zoom_out)
        rotate_90_btn.clicked.connect(lambda: self.rotate_page(90))
        rotate_neg_90_btn.clicked.connect(lambda: self.rotate_page(-90))
        fullscreen_btn.clicked.connect(self.toggle_fullscreen)

        # Setup keyboard shortcut for full screen
        self.shortcut_fullscreen = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

        # Setup Escape key to exit full screen
        self.shortcut_exit_fullscreen = QShortcut(QKeySequence("Esc"), self)
        self.shortcut_exit_fullscreen.activated.connect(self.exit_fullscreen)

        # Setup keyboard shortcuts for zoom
        self.shortcut_zoom_in = QShortcut(QKeySequence("Ctrl++"), self)
        self.shortcut_zoom_in.activated.connect(self.zoom_in)
        self.shortcut_zoom_in_alt = QShortcut(
            QKeySequence("Ctrl+="), self
        )  # For keyboards where + requires Shift
        self.shortcut_zoom_in_alt.activated.connect(self.zoom_in)

        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(self.zoom_out)

        # Setup keyboard shortcut for zoom level dialog
        self.shortcut_zoom_level = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_zoom_level.activated.connect(self.show_zoom_dialog)

        # Setup keyboard shortcuts for rotation
        self.shortcut_rotate_90 = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut_rotate_90.activated.connect(lambda: self.rotate_page(90))
        self.shortcut_rotate_neg_90 = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        self.shortcut_rotate_neg_90.activated.connect(lambda: self.rotate_page(-90))

        # Setup keyboard shortcut for invert
        self.shortcut_invert = QShortcut(QKeySequence("Ctrl+I"), self)
        self.shortcut_invert.activated.connect(self.toggle_invert)

    def open_pdf(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", "", "PDF Files (*.pdf)"
        )
        if file_name:
            self.current_doc = fitz.open(file_name)
            self.current_page = self.current_doc[0]  # First page
            self.display_page()

    def display_page(self):
        if not self.current_page:
            return

        # Store the current scroll position and viewport size for both views
        normal_scroll_pos = self.normal_scroll_area.verticalScrollBar().value()
        normal_viewport_height = self.normal_scroll_area.viewport().height()
        normal_content_height = self.normal_image_label.height()

        fullscreen_scroll_pos = self.fullscreen_scroll_area.verticalScrollBar().value()
        fullscreen_viewport_height = self.fullscreen_scroll_area.viewport().height()
        fullscreen_content_height = self.fullscreen_image_label.height()

        # Calculate relative positions (0 to 1)
        if normal_content_height > normal_viewport_height:
            normal_relative_pos = (
                normal_scroll_pos + normal_viewport_height / 2
            ) / normal_content_height
        else:
            normal_relative_pos = 0.5

        if fullscreen_content_height > fullscreen_viewport_height:
            fullscreen_relative_pos = (
                fullscreen_scroll_pos + fullscreen_viewport_height / 2
            ) / fullscreen_content_height
        else:
            fullscreen_relative_pos = 0.5

        # Render page with current zoom and rotation
        matrix = fitz.Matrix(self.zoom_level, self.zoom_level).prerotate(self.rotation)
        pix = self.current_page.get_pixmap(matrix=matrix)

        # Convert to QImage
        img = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
        )

        if self.is_inverted:
            img.invertPixels()  # Invert the colors

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(img)

        # Display in both views
        self.normal_image_label.setPixmap(pixmap)
        self.normal_image_label.adjustSize()
        self.fullscreen_image_label.setPixmap(pixmap)
        self.fullscreen_image_label.adjustSize()

        # Restore the relative scroll positions
        if normal_content_height > normal_viewport_height:
            new_normal_scroll_pos = int(
                normal_relative_pos * self.normal_image_label.height()
                - normal_viewport_height / 2
            )
            self.normal_scroll_area.verticalScrollBar().setValue(new_normal_scroll_pos)

        if fullscreen_content_height > fullscreen_viewport_height:
            new_fullscreen_scroll_pos = int(
                fullscreen_relative_pos * self.fullscreen_image_label.height()
                - fullscreen_viewport_height / 2
            )
            self.fullscreen_scroll_area.verticalScrollBar().setValue(
                new_fullscreen_scroll_pos
            )

        # Do the same for horizontal scrolling
        normal_scroll_x = self.normal_scroll_area.horizontalScrollBar().value()
        normal_viewport_width = self.normal_scroll_area.viewport().width()
        normal_content_width = self.normal_image_label.width()

        fullscreen_scroll_x = self.fullscreen_scroll_area.horizontalScrollBar().value()
        fullscreen_viewport_width = self.fullscreen_scroll_area.viewport().width()
        fullscreen_content_width = self.fullscreen_image_label.width()

        if normal_content_width > normal_viewport_width:
            normal_relative_x = (
                normal_scroll_x + normal_viewport_width / 2
            ) / normal_content_width
            new_normal_scroll_x = int(
                normal_relative_x * self.normal_image_label.width()
                - normal_viewport_width / 2
            )
            self.normal_scroll_area.horizontalScrollBar().setValue(new_normal_scroll_x)

        if fullscreen_content_width > fullscreen_viewport_width:
            fullscreen_relative_x = (
                fullscreen_scroll_x + fullscreen_viewport_width / 2
            ) / fullscreen_content_width
            new_fullscreen_scroll_x = int(
                fullscreen_relative_x * self.fullscreen_image_label.width()
                - fullscreen_viewport_width / 2
            )
            self.fullscreen_scroll_area.horizontalScrollBar().setValue(
                new_fullscreen_scroll_x
            )

    def show_zoom_dialog(self):
        """Show dialog for entering custom zoom level"""
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Set Zoom Level")
        dialog.setLabelText("Enter zoom level (0.001 to 5.000):")

        # Use text input mode for precise decimal handling
        dialog.setInputMode(QInputDialog.TextInput)

        # Set current zoom level as default with 3 decimal places
        dialog.setTextValue(f"{self.zoom_level:.3f}")

        # Create and populate combobox with zoom history
        if hasattr(dialog, "findChild"):
            combo = dialog.findChild(QComboBox)
            if combo:
                combo.addItems([f"{zoom:.3f}" for zoom in self.zoom_history])

        if dialog.exec_():
            try:
                new_zoom = float(dialog.textValue())
                if 0.001 <= new_zoom <= 5.000:
                    # Add to history if not already present
                    if new_zoom not in self.zoom_history:
                        self.zoom_history.append(new_zoom)
                        # Keep only the last 10 values
                        self.zoom_history = self.zoom_history[-10:]
                        # Save to settings
                        self.settings.setValue("zoom_history", self.zoom_history)

                    # Apply the new zoom level
                    self.zoom_level = new_zoom
                    self.display_page()
                else:
                    QMessageBox.warning(
                        self,
                        "Invalid Zoom Level",
                        "Please enter a value between 0.001 and 5.000",
                    )
            except ValueError:
                QMessageBox.warning(
                    self, "Invalid Input", "Please enter a valid number (e.g., 0.125)"
                )

    def zoom_in(self):
        """Zoom in by 0.1"""
        self.zoom_level = min(5.000, self.zoom_level + 0.1)
        self.display_page()

    def zoom_out(self):
        """Zoom out by 0.1"""
        self.zoom_level = max(0.001, self.zoom_level - 0.1)
        self.display_page()

    def rotate_page(self, angle):
        """Rotate the page by the specified angle (90, 180, or 270 degrees)"""
        self.rotation = (self.rotation + angle) % 360
        self.display_page()

    def toggle_fullscreen(self):
        """Toggle between fullscreen view of the PDF and normal mode"""
        if not self.is_fullscreen:
            # Switch to fullscreen view
            self.stacked_widget.setCurrentIndex(1)
            self.showFullScreen()
            self.is_fullscreen = True
        else:
            self.exit_fullscreen()

    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            # Switch back to normal view
            self.stacked_widget.setCurrentIndex(0)
            self.showNormal()
            self.is_fullscreen = False

    def toggle_invert(self):
        """Toggle between normal and inverted colors"""
        self.is_inverted = not self.is_inverted
        self.display_page()


def main():
    app = QApplication(sys.argv)
    reader = PDFReader()
    reader.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
