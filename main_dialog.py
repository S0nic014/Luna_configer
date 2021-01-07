import timeit
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
import pymel.api as pma
import pymel.core as pm
from shiboken2 import getCppPointer
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from Luna import Logger
from Luna import Config
from Luna import LunaVars
from Luna_configer import pages
from Luna.utils import pysideFn
reload(pages)

DEBUG = Logger.get_level() == 10


class MainDialog(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    WINDOW_TITLE = "Luna configuaration"
    UI_NAME = "LunaConfigManager"
    MINIMUM_SIZE = [400, 500]
    GEOMETRY = None

    def __init__(self):
        super(MainDialog, self).__init__()

        # Window adjustments
        self.setObjectName(self.__class__.UI_NAME)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(*self.MINIMUM_SIZE)
        self.setMaximumHeight(600)
        # MacOSX window stay on top
        self.setProperty("saveWindowPref", True)
        self.setWindowIcon(pysideFn.get_QIcon("config.svg"))

        # UI setup
        self.create_actions()
        self.create_menu_bar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.update_configs()

        # Load geo and show
        self.restoreGeometry(MainDialog.GEOMETRY)
        self.show()

    def create_actions(self):
        self.reset_configs_action = QtWidgets.QAction("Restore default config", self)
        self.documentation_action = QtWidgets.QAction("Documentation", self)
        self.documentation_action.setIcon(QtGui.QIcon(":help.png"))

    def create_menu_bar(self):
        # Edit menu
        edit_menu = QtWidgets.QMenu("&Edit")
        edit_menu.addAction(self.reset_configs_action)
        # Help menu
        help_menu = QtWidgets.QMenu("Help")
        help_menu.addAction(self.documentation_action)
        # Menubar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.addMenu(edit_menu)
        self.menu_bar.addMenu(help_menu)

    def create_widgets(self):
        # Top right button
        self.reload_config_btn = QtWidgets.QPushButton()
        self.reload_config_btn.setFlat(True)
        self.reload_config_btn.setIcon(pysideFn.get_QIcon("refresh.png"))
        self.menu_bar.setCornerWidget(self.reload_config_btn, QtCore.Qt.TopRightCorner)

        # Create stack, list widgets
        self.stack_wgt = QtWidgets.QStackedWidget()
        self.category_list = QtWidgets.QListWidget()
        self.category_list.setMaximumWidth(180)
        self.config_splitter = QtWidgets.QSplitter()
        self.config_splitter.addWidget(self.category_list)
        self.config_splitter.addWidget(self.stack_wgt)

        # Create pages
        self.dev_page = pages.DeveloperPage()

        # Populate stack
        self.stack_wgt.addWidget(self.dev_page)

        # Populate category
        for child in self.stack_wgt.children():
            if isinstance(child, pages.PageWidget):
                category_item = QtWidgets.QListWidgetItem()
                category_item.setText(child.category_name)
                self.category_list.addItem(category_item)

        # Action buttons
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setMinimumWidth(90)
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(90)

    def create_layouts(self):
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setMenuBar(self.menu_bar)
        self.main_layout.addWidget(self.config_splitter)
        self.main_layout.addLayout(self.buttons_layout)

    def create_connections(self):
        self.reload_config_btn.clicked.connect(self.update_configs)
        self.category_list.currentRowChanged.connect(self.stack_wgt.setCurrentIndex)
        self.reset_configs_action.triggered.connect(Config.reset)
        self.save_button.clicked.connect(self.save_configs)
        self.cancel_button.clicked.connect(self.close)

    def save_configs(self):
        for child in self.stack_wgt.children():
            if isinstance(child, pages.PageWidget):
                child.save_config()
        self.close()
        self.deleteLater()

    def update_configs(self):
        start_time = timeit.default_timer()
        for child in self.stack_wgt.children():
            if isinstance(child, pages.PageWidget):
                child.load_config()
                Logger.debug("{0} page - loaded in: {1}s".format(child.category_name, timeit.default_timer() - start_time))
        Logger.debug("Config load time: {0}s".format(timeit.default_timer() - start_time))

    def closeEvent(self, event):
        super(MainDialog, self).closeEvent(event)
        MainDialog.GEOMETRY = self.saveGeometry()


if __name__ == "__main__":
    testTool = MainDialog()
    testTool.show(dockable=0)
