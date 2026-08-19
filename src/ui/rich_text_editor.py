import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QToolBar,
    QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QLineEdit, QDialog, QFontComboBox,
    QComboBox, QColorDialog, QFileDialog, QMainWindow
)
from PySide6.QtGui import (
    QAction, QTextCharFormat, QFont, QColor,
    QTextCursor, QKeySequence, QTextListFormat,
    QTextTableFormat, QDesktopServices
)
from PySide6.QtCore import Qt, QUrl, Signal


# ------------------------------------------------------------------ #
#  Dialogues utilitaires                                               #
# ------------------------------------------------------------------ #
class LinkDialog(QDialog):
    def __init__(self, parent=None, url="", text=""):
        super().__init__(parent)
        self.setWindowTitle("Lien hypertexte")
        self.setFixedSize(400, 150)
        layout = QVBoxLayout(self)

        text_row = QHBoxLayout()
        text_row.addWidget(QLabel("Texte affiché :"))
        self.text_edit = QLineEdit(text)
        self.text_edit.setPlaceholderText("Laisser vide = garder la sélection")
        text_row.addWidget(self.text_edit)
        layout.addLayout(text_row)

        url_row = QHBoxLayout()
        url_row.addWidget(QLabel("URL :          "))
        self.url_edit = QLineEdit(url)
        self.url_edit.setPlaceholderText("https://example.com")
        url_row.addWidget(self.url_edit)
        layout.addLayout(url_row)

        btn_row = QHBoxLayout()
        ok = QPushButton("Insérer")
        ok.setDefault(True)
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Annuler")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(ok)
        btn_row.addWidget(cancel)
        layout.addLayout(btn_row)

    def values(self):
        return self.url_edit.text().strip(), self.text_edit.text().strip()


class TableDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insérer un tableau")
        self.setFixedSize(260, 140)
        layout = QVBoxLayout(self)

        for label, attr, default in [("Lignes :", "rows_spin", 3),
                                      ("Colonnes :", "cols_spin", 3)]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            spin = QSpinBox()
            spin.setRange(1, 20)
            spin.setValue(default)
            setattr(self, attr, spin)
            row.addWidget(spin)
            layout.addLayout(row)

        btn_row = QHBoxLayout()
        ok = QPushButton("Insérer")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Annuler")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(ok)
        btn_row.addWidget(cancel)
        layout.addLayout(btn_row)

    def values(self):
        return self.rows_spin.value(), self.cols_spin.value()


# ------------------------------------------------------------------ #
#  Zone de texte avec gestion des liens                               #
# ------------------------------------------------------------------ #
class _LinkAwareTextEdit(QTextEdit):
    """QTextEdit interne : Ctrl+clic ouvre les liens, clic droit les gère."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.modifiers() & Qt.ControlModifier:
            anchor = self.anchorAt(event.pos())
            if anchor:
                QDesktopServices.openUrl(QUrl(anchor))
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        anchor = self.anchorAt(event.pos())
        self.viewport().setCursor(
            Qt.PointingHandCursor if anchor else Qt.IBeamCursor
        )
        super().mouseMoveEvent(event)

    def contextMenuEvent(self, event):
        anchor = self.anchorAt(event.pos())
        menu = self.createStandardContextMenu()

        if anchor:
            menu.addSeparator()
            act_open = QAction(f"Ouvrir : {anchor}", menu)
            act_open.triggered.connect(
                lambda: QDesktopServices.openUrl(QUrl(anchor))
            )
            menu.addAction(act_open)

            act_edit = QAction("Modifier le lien…", menu)
            act_edit.triggered.connect(
                lambda: self._request_edit_link(event.pos())
            )
            menu.addAction(act_edit)

            act_rm = QAction("Supprimer le lien", menu)
            act_rm.triggered.connect(
                lambda: self._remove_link_at(event.pos())
            )
            menu.addAction(act_rm)

        menu.exec(event.globalPos())

    # -- helpers internes --
    def _anchor_cursor(self, pos):
        """Retourne un curseur sélectionnant tout le fragment du lien en pos."""
        anchor = self.anchorAt(pos)
        if not anchor:
            return None

        def _char_anchor(cur):
            c = self.document().characterAt(cur.position())
            tmp = QTextCursor(self.document())
            tmp.setPosition(cur.position())
            return tmp.charFormat().anchorHref()

        cursor = self.cursorForPosition(pos)
        pos_in_doc = cursor.position()

        # Reculer
        start = pos_in_doc
        while start > 0:
            tmp = QTextCursor(self.document())
            tmp.setPosition(start - 1)
            if tmp.charFormat().anchorHref() != anchor:
                break
            start -= 1

        # Avancer
        end = pos_in_doc
        doc_len = self.document().characterCount()
        while end < doc_len - 1:
            tmp = QTextCursor(self.document())
            tmp.setPosition(end)
            if tmp.charFormat().anchorHref() != anchor:
                break
            end += 1

        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        return cursor

    def _request_edit_link(self, pos):
        anchor = self.anchorAt(pos)
        cursor = self._anchor_cursor(pos)
        if cursor is None:
            return
        text = cursor.selectedText()
        dlg = LinkDialog(self, url=anchor, text=text)
        if dlg.exec() != QDialog.Accepted:
            return
        new_url, new_text = dlg.values()
        if not new_url:
            return
        if not new_url.startswith(("http://", "https://", "mailto:", "ftp://")):
            new_url = "https://" + new_url
        fmt = QTextCharFormat()
        fmt.setAnchor(True)
        fmt.setAnchorHref(new_url)
        fmt.setForeground(QColor("#1a6fc4"))
        fmt.setFontUnderline(True)
        cursor.removeSelectedText()
        cursor.insertText(new_text or text, fmt)
        self.setTextCursor(cursor)

    def _remove_link_at(self, pos):
        cursor = self._anchor_cursor(pos)
        if cursor is None:
            return
        text = cursor.selectedText()
        fmt = QTextCharFormat()
        fmt.setAnchor(False)
        fmt.setAnchorHref("")
        fmt.setForeground(QColor())
        fmt.setFontUnderline(False)
        cursor.removeSelectedText()
        cursor.insertText(text, fmt)
        self.setTextCursor(cursor)


# ------------------------------------------------------------------ #
#  Widget principal — à inclure dans n'importe quel formulaire        #
# ------------------------------------------------------------------ #
class RichTextEditor(QWidget):
    """
    Éditeur de texte riche autonome, utilisable comme n'importe quel QWidget.

    Signaux :
        text_changed()  — émis à chaque modification du contenu

    Méthodes publiques :
        to_html()           -> str   : contenu en HTML
        set_html(html: str)          : charge du HTML
        to_plain_text()     -> str   : texte brut sans balises
        clear()                      : vide l'éditeur
        set_placeholder(text: str)   : texte d'aide affiché quand vide
    """

    text_changed = Signal()

    def __init__(self, parent=None, *, placeholder="Saisissez votre texte ici…"):
        super().__init__(parent)
        self._build_ui(placeholder)
        self._connect_signals()

    # ------------------------------------------------------------------ #
    #  Construction de l'UI                                               #
    # ------------------------------------------------------------------ #
    def _build_ui(self, placeholder):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # -- Barre d'outils --
        self._toolbar = QToolBar()
        self._toolbar.setMovable(False)
        root.addWidget(self._toolbar)
        self._fill_toolbar()

        # -- Éditeur --
        self._editor = _LinkAwareTextEdit()
        self._editor.setPlaceholderText(placeholder)
        self._editor.setFontPointSize(12)
        root.addWidget(self._editor)

    def _fill_toolbar(self):
        tb = self._toolbar

        # Police
        self._font_combo = QFontComboBox()
        tb.addWidget(self._font_combo)

        self._size_combo = QComboBox()
        self._size_combo.addItems(
            ["8","10","11","12","14","16","18","24","36","48","72"]
        )
        self._size_combo.setCurrentText("12")
        tb.addWidget(self._size_combo)

        tb.addSeparator()

        # Gras / Italique / Souligné / Barré
        self._act_bold = self._checkable_action("G", "Gras (Ctrl+B)", QKeySequence.Bold)
        self._act_italic = self._checkable_action("I", "Italique (Ctrl+I)", QKeySequence.Italic)
        self._act_underline = self._checkable_action("U", "Souligné (Ctrl+U)", QKeySequence.Underline)
        self._act_strike = self._checkable_action("S̶", "Barré")

        for act in (self._act_bold, self._act_italic,
                    self._act_underline, self._act_strike):
            tb.addAction(act)

        tb.addSeparator()

        # Couleur
        act_color = QAction("Couleur…", self)
        act_color.setToolTip("Couleur du texte")
        act_color.triggered.connect(self._choose_color)
        tb.addAction(act_color)

        tb.addSeparator()

        # Alignement
        for label, alignment in [
            ("◀", Qt.AlignLeft), ("▬", Qt.AlignCenter),
            ("▶", Qt.AlignRight), ("≡", Qt.AlignJustify),
        ]:
            act = QAction(label, self)
            act.triggered.connect(
                lambda _, a=alignment: self._editor.setAlignment(a)
            )
            tb.addAction(act)

        tb.addSeparator()

        # Listes
        act_ul = QAction("• Puces", self)
        act_ul.triggered.connect(self._insert_bullet_list)
        tb.addAction(act_ul)

        act_ol = QAction("1. Numéros", self)
        act_ol.triggered.connect(self._insert_ordered_list)
        tb.addAction(act_ol)

        act_indent = QAction("→", self)
        act_indent.setToolTip("Indenter (Tab)")
        act_indent.setShortcut("Tab")
        act_indent.triggered.connect(self._indent_list)
        tb.addAction(act_indent)

        act_dedent = QAction("←", self)
        act_dedent.setToolTip("Désindenter (Shift+Tab)")
        act_dedent.setShortcut("Shift+Tab")
        act_dedent.triggered.connect(self._dedent_list)
        tb.addAction(act_dedent)

        tb.addSeparator()

        # Tableau
        act_table = QAction("⊞ Tableau", self)
        act_table.triggered.connect(self._insert_table)
        tb.addAction(act_table)

        act_add_row = QAction("+L", self)
        act_add_row.setToolTip("Ajouter une ligne")
        act_add_row.triggered.connect(self._table_add_row)
        tb.addAction(act_add_row)

        act_add_col = QAction("+C", self)
        act_add_col.setToolTip("Ajouter une colonne")
        act_add_col.triggered.connect(self._table_add_col)
        tb.addAction(act_add_col)

        act_del_row = QAction("−L", self)
        act_del_row.setToolTip("Supprimer la ligne")
        act_del_row.triggered.connect(self._table_del_row)
        tb.addAction(act_del_row)

        act_del_col = QAction("−C", self)
        act_del_col.setToolTip("Supprimer la colonne")
        act_del_col.triggered.connect(self._table_del_col)
        tb.addAction(act_del_col)

        tb.addSeparator()

        # Lien
        self._act_link = self._checkable_action(
            "🔗 Lien…", "Insérer / modifier un lien (Ctrl+K)", "Ctrl+K"
        )
        self._act_link.triggered.connect(self._insert_or_edit_link)
        tb.addAction(self._act_link)

        act_rm_link = QAction("✂ Suppr. lien", self)
        act_rm_link.setToolTip("Supprimer le lien sous le curseur")
        act_rm_link.triggered.connect(self._remove_link_at_cursor)
        tb.addAction(act_rm_link)

    def _checkable_action(self, label, tooltip="", shortcut=None):
        act = QAction(label, self)
        act.setCheckable(True)
        act.setToolTip(tooltip)
        if shortcut:
            act.setShortcut(shortcut)
        return act

    # ------------------------------------------------------------------ #
    #  Connexions                                                          #
    # ------------------------------------------------------------------ #
    def _connect_signals(self):
        self._font_combo.currentFontChanged.connect(
            lambda f: self._editor.setCurrentFont(f)
        )
        self._size_combo.currentTextChanged.connect(
            lambda s: self._editor.setFontPointSize(float(s))
        )
        self._act_bold.triggered.connect(
            lambda checked: self._editor.setFontWeight(
                QFont.Bold if checked else QFont.Normal
            )
        )
        self._act_italic.triggered.connect(self._editor.setFontItalic)
        self._act_underline.triggered.connect(self._editor.setFontUnderline)
        self._act_strike.triggered.connect(self._toggle_strikethrough)

        self._editor.currentCharFormatChanged.connect(self._sync_toolbar)
        self._editor.textChanged.connect(self.text_changed)

    # ------------------------------------------------------------------ #
    #  Synchronisation barre d'outils                                     #
    # ------------------------------------------------------------------ #
    def _sync_toolbar(self, fmt: QTextCharFormat):
        self._act_bold.setChecked(fmt.fontWeight() == QFont.Bold)
        self._act_italic.setChecked(fmt.fontItalic())
        self._act_underline.setChecked(fmt.fontUnderline())
        self._act_strike.setChecked(fmt.fontStrikeOut())
        self._act_link.setChecked(bool(fmt.anchorHref()))

        fonts = fmt.fontFamilies()
        if fonts:
            self._font_combo.setCurrentFont(QFont(fonts[0]))
        size = fmt.fontPointSize()
        if size > 0:
            self._size_combo.setCurrentText(str(int(size)))

    # ------------------------------------------------------------------ #
    #  Formatage                                                           #
    # ------------------------------------------------------------------ #
    def _toggle_strikethrough(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(checked)
        self._editor.mergeCurrentCharFormat(fmt)

    def _choose_color(self):
        color = QColorDialog.getColor(self._editor.textColor(), self)
        if color.isValid():
            self._editor.setTextColor(color)

    # ------------------------------------------------------------------ #
    #  Listes                                                              #
    # ------------------------------------------------------------------ #
    def _insert_bullet_list(self):
        cursor = self._editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDisc)
        fmt.setIndent(1)
        cursor.createList(fmt)

    def _insert_ordered_list(self):
        cursor = self._editor.textCursor()
        fmt = QTextListFormat()
        fmt.setStyle(QTextListFormat.ListDecimal)
        fmt.setIndent(1)
        cursor.createList(fmt)

    def _indent_list(self):
        lst = self._editor.textCursor().currentList()
        if lst:
            fmt = lst.format()
            fmt.setIndent(fmt.indent() + 1)
            lst.setFormat(fmt)

    def _dedent_list(self):
        lst = self._editor.textCursor().currentList()
        if lst:
            fmt = lst.format()
            fmt.setIndent(max(1, fmt.indent() - 1))
            lst.setFormat(fmt)

    # ------------------------------------------------------------------ #
    #  Tableaux                                                            #
    # ------------------------------------------------------------------ #
    def _insert_table(self):
        dlg = TableDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return
        rows, cols = dlg.values()
        cursor = self._editor.textCursor()
        fmt = QTextTableFormat()
        fmt.setCellPadding(6)
        fmt.setCellSpacing(0)
        fmt.setBorder(1)
        fmt.setBorderStyle(QTextTableFormat.BorderStyle_Solid)
        fmt.setWidth(600)
        cursor.insertTable(rows, cols, fmt)

    def _current_table(self):
        return self._editor.textCursor().currentTable()

    def _table_add_row(self):
        t = self._current_table()
        if t:
            t.insertRows(t.cellAt(self._editor.textCursor()).row() + 1, 1)

    def _table_add_col(self):
        t = self._current_table()
        if t:
            t.insertColumns(t.cellAt(self._editor.textCursor()).column() + 1, 1)

    def _table_del_row(self):
        t = self._current_table()
        if t and t.rows() > 1:
            t.removeRows(t.cellAt(self._editor.textCursor()).row(), 1)

    def _table_del_col(self):
        t = self._current_table()
        if t and t.columns() > 1:
            t.removeColumns(t.cellAt(self._editor.textCursor()).column(), 1)

    # ------------------------------------------------------------------ #
    #  Liens                                                               #
    # ------------------------------------------------------------------ #
    def _insert_or_edit_link(self):
        cursor = self._editor.textCursor()
        existing_url = cursor.charFormat().anchorHref()
        existing_text = cursor.selectedText()

        dlg = LinkDialog(self, url=existing_url, text=existing_text)
        if dlg.exec() != QDialog.Accepted:
            return

        url, text = dlg.values()
        if not url:
            return
        if not url.startswith(("http://", "https://", "mailto:", "ftp://")):
            url = "https://" + url

        display = text or existing_text or url

        fmt = QTextCharFormat()
        fmt.setAnchor(True)
        fmt.setAnchorHref(url)
        fmt.setForeground(QColor("#1a6fc4"))
        fmt.setFontUnderline(True)

        if cursor.hasSelection():
            cursor.mergeCharFormat(fmt)
        else:
            cursor.insertText(display, fmt)

        # Format neutre après le lien
        neutral = QTextCharFormat()
        neutral.setAnchor(False)
        neutral.setAnchorHref("")
        neutral.setForeground(QColor())
        neutral.setFontUnderline(False)
        cursor.setPosition(cursor.selectionEnd())
        cursor.setCharFormat(neutral)
        self._editor.setTextCursor(cursor)

    def _remove_link_at_cursor(self):
        cursor = self._editor.textCursor()
        if not cursor.charFormat().anchorHref():
            return
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        fmt = QTextCharFormat()
        fmt.setAnchor(False)
        fmt.setAnchorHref("")
        fmt.setForeground(QColor())
        fmt.setFontUnderline(False)
        cursor.mergeCharFormat(fmt)
        self._editor.setTextCursor(cursor)

    # ------------------------------------------------------------------ #
    #  API publique                                                        #
    # ------------------------------------------------------------------ #
    def to_html(self) -> str:
        """Retourne le contenu de l'éditeur en HTML."""
        return self._editor.toHtml()

    def set_html(self, html: str):
        """Charge du contenu HTML dans l'éditeur."""
        self._editor.setHtml(html)

    def to_plain_text(self) -> str:
        """Retourne le contenu sans aucune balise."""
        return self._editor.toPlainText()

    def clear(self):
        """Vide l'éditeur."""
        self._editor.clear()

    def set_placeholder(self, text: str):
        """Définit le texte d'aide affiché quand l'éditeur est vide."""
        self._editor.setPlaceholderText(text)


# ------------------------------------------------------------------ #
#  Exemple d'intégration dans un formulaire                           #
# ------------------------------------------------------------------ #
class ExampleForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemple — formulaire avec RichTextEditor")
        self.resize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Champ titre classique
        title_row = QHBoxLayout()
        title_row.addWidget(QLabel("Titre :"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titre de l'article…")
        title_row.addWidget(self.title_input)
        layout.addLayout(title_row)

        # Notre widget éditeur riche
        layout.addWidget(QLabel("Contenu :"))
        self.editor = RichTextEditor(
            placeholder="Rédigez le contenu ici…"
        )
        layout.addWidget(self.editor, stretch=1)

        # Boutons d'action du formulaire
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_save = QPushButton("Enregistrer HTML…")
        btn_save.clicked.connect(self._save)
        btn_row.addWidget(btn_save)

        btn_load = QPushButton("Charger HTML…")
        btn_load.clicked.connect(self._load)
        btn_row.addWidget(btn_load)

        btn_clear = QPushButton("Effacer")
        btn_clear.clicked.connect(self.editor.clear)
        btn_row.addWidget(btn_clear)

        layout.addLayout(btn_row)

        # Réagir aux changements
        self.editor.text_changed.connect(self._on_change)

    def _on_change(self):
        title = self.title_input.text() or "Sans titre"
        self.setWindowTitle(f"Formulaire — {title} *")

    def _save(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer", "", "HTML (*.html)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.to_html())

    def _load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir", "", "HTML (*.html)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.editor.set_html(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ExampleForm()
    win.show()
    sys.exit(app.exec())