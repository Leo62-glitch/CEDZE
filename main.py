# ici j'importe tous les modules nécessaires
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

# pour éviter de créer des fenêtres supplémentaires, on vérifie si l'application a déjà une instance ouverte
application = QApplication.instance()
# si il n'y a pas d'instance, on en crée une
if not application:
    application = QApplication(sys.argv)

# Charge le fichier local index.html
local_path = os.path.abspath("index.html")

# Fenêtre principale
class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Titre et dimensions de la fenêtre
        self.setWindowTitle("CEDZEE Browser")
        self.resize(1200, 800)
        self.move(300, 50)

        # Création du widget d'onglets
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)  # Fermer l'onglet avec le bouton
        self.setCentralWidget(self.tabs)

        # Menu de navigation
        self.menu = QToolBar("Menu de navigation")
        self.addToolBar(self.menu)

        # Boutons de navigation
        self.add_navigation_buttons()

        # Ajout d'un premier onglet par défaut
        self.add_new_tab(QUrl.fromLocalFile(local_path), "Nouvel Onglet")

    def add_navigation_buttons(self):
        """Ajoute les boutons de navigation au menu."""
        # Bouton Précédent
        back_btn = QAction("←", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        self.menu.addAction(back_btn)

        # Bouton Suivant
        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.menu.addAction(forward_btn)

        # Bouton Recharger
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.menu.addAction(reload_btn)

        # Bouton Home
        home_btn = QAction("⌂", self)
        home_btn.triggered.connect(self.go_home)
        self.menu.addAction(home_btn)

        # Barre d'adresse
        self.adress_input = QLineEdit()
        self.adress_input.returnPressed.connect(self.navigate_to_url)
        self.menu.addWidget(self.adress_input)

        # Bouton Nouvel Onglet
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(self.open_new_tab)
        self.menu.addAction(new_tab_btn)

    def add_new_tab(self, url, label="Nouvel Onglet"):
        """Ajoute un nouvel onglet au navigateur."""
        browser = QWebEngineView()
        browser.setUrl(url)
        browser.urlChanged.connect(self.update_urlbar)  # Mettre à jour la barre d'adresse
        browser.loadFinished.connect(lambda: self.tabs.setTabText(self.tabs.currentIndex(), browser.page().title()))  # Mettre à jour le titre de l'onglet

        # Création d'un conteneur pour l'onglet
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)

        self.tabs.addTab(tab, label)
        self.tabs.setCurrentWidget(tab)

    def current_browser(self):
        """Renvoie l'instance actuelle de QWebEngineView."""
        current_tab = self.tabs.currentWidget()
        return current_tab.layout().itemAt(0).widget()

    def close_tab(self, index):
        """Ferme l'onglet à l'index spécifié."""
        if self.tabs.count() > 1:  # Ne pas fermer le dernier onglet
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        """Navigue vers l'URL saisie dans la barre d'adresse."""
        url = QUrl(self.adress_input.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.current_browser().setUrl(url)

    def update_urlbar(self, url):
        """Met à jour la barre d'adresse avec l'URL actuelle."""
        self.adress_input.setText(url.toString())
        self.adress_input.setCursorPosition(0)

    def go_home(self):
        """Navigue vers la page d'accueil (index.html)."""
        self.current_browser().setUrl(QUrl.fromLocalFile(local_path))

    def open_new_tab(self):
        """Ouvre un nouvel onglet."""
        self.add_new_tab(QUrl.fromLocalFile(local_path), "Nouvel Onglet")


# On crée une instance de la fenêtre principale et on l'affiche
window = BrowserWindow()
window.show()

# On exécute l'application
application.exec_()
