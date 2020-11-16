from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
import pymel.api as pma
import pymel.core as pm
from shiboken2 import getCppPointer
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from Luna import Logger
from Luna import Config
from Luna_configer import pages
from Luna.utils import pysideFn
reload(pages)


class MainDialog(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    WINDOW_TITLE = "Luna configuaration"
    UI_NAME = "LunaConfigManager"
    UI_SCRIPT = "import Luna_configer\nLuna_configer.MainDialog()"
    UI_INSTANCE = None
    MINIMUM_SIZE = [400, 500]

    @classmethod
    def display(cls):
        if not cls.UI_INSTANCE:
            cls.UI_INSTANCE = MainDialog()

        if cls.UI_INSTANCE.isHidden():
            cls.UI_INSTANCE.show(dockable=1, uiScript=cls.UI_SCRIPT)
        else:
            cls.UI_INSTANCE.raise_()
            cls.UI_INSTANCE.activateWindow()

    def __init__(self):
        super(MainDialog, self).__init__()

        # Window adjustments
        self.__class__.UI_INSTANCE = self
        self.setObjectName(self.__class__.UI_NAME)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(*self.MINIMUM_SIZE)
        self.setMaximumHeight(600)

        # Workspace control
        self.workspaceControlName = "{0}WorkspaceControl".format(self.UI_NAME)
        if pm.workspaceControl(self.workspaceControlName, q=1, ex=1):
            workspaceControlPtr = long(pma.MQtUtil.findControl(self.workspaceControlName))
            widgetPtr = long(getCppPointer(self)[0])
            pma.MQtUtil.addWidgetToMayaLayout(widgetPtr, workspaceControlPtr)

        # UI setup
        self.create_actions()
        self.create_menu_bar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.update_configs()

    def create_actions(self):
        self.reset_configs_action = QtWidgets.QAction("Restore default config", self)
        self.documentation_action = QtWidgets.QAction("Documentation", self)
        self.documentation_action.setIcon(QtGui.QIcon(":help.png"))
        self.update_configs_action = QtWidgets.QAction("", self)
        self.update_configs_action.setIcon(QtGui.QIcon(pysideFn.getIcon("refresh.png")))

    def create_menu_bar(self):
        # self.menuBar.setCornerWidget(self.right_menu_bar)
        # self.menuBar.addAction(self.update_configs_action)
        # Edit menu
        edit_menu = QtWidgets.QMenu("&Edit")
        edit_menu.addAction(self.reset_configs_action)
        # Help menu
        help_menu = QtWidgets.QMenu("Help")
        help_menu.addAction(self.documentation_action)
        # Menubar
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.addMenu(edit_menu)
        self.menuBar.addMenu(help_menu)

        # Right menubar
        self.right_menu_bar = QtWidgets.QMenuBar(self.menuBar)
        self.right_menu_bar.addAction(self.update_configs_action)
        self.menuBar.setCornerWidget(self.right_menu_bar, QtCore.Qt.TopRightCorner)

    def create_widgets(self):
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
        self.main_layout.setMenuBar(self.menuBar)
        self.main_layout.addWidget(self.config_splitter)
        self.main_layout.addLayout(self.buttons_layout)

    def create_connections(self):
        self.category_list.currentRowChanged.connect(self.stack_wgt.setCurrentIndex)
        self.reset_configs_action.triggered.connect(Config.reset)
        self.update_configs_action.triggered.connect(self.update_configs)
        self.save_button.clicked.connect(self.save_configs)
        self.cancel_button.clicked.connect(self.close)

    def save_configs(self):
        for child in self.stack_wgt.children():
            if isinstance(child, pages.PageWidget):
                child.save_config()
        self.hide()

    def update_configs(self):
        for child in self.stack_wgt.children():
            if isinstance(child, pages.PageWidget):
                child.load_config()


if __name__ == "__main__":
    try:
        if testTool and testTool.parent():  # noqa: F821
            workspaceControlName = testTool.parent().objectName()  # noqa: F821

            if pm.window(workspaceControlName, ex=1, q=1):
                pm.deleteUI(workspaceControlName)
    except Exception:
        pass

    testTool = MainDialog()
    testTool.show(dockable=1, uiScript=testTool.UI_SCRIPT)
