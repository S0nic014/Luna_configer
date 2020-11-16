from PySide2 import QtWidgets
from Luna import Logger
from Luna import Config
from Luna import LunaVars
from Luna import TestVars
from Luna.interface import shared_widgets
reload(shared_widgets)


class PageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, category_name="Category"):
        super(PageWidget, self).__init__(parent)
        self.category_name = category_name

    def load_config(self):
        raise NotImplementedError

    def save_config(self):
        raise NotImplementedError


class DeveloperPage(PageWidget):
    def __init__(self, parent=None, category_name="Developer"):
        super(DeveloperPage, self).__init__(parent=parent, category_name=category_name)

        self._create_widgets()
        self._create_layous()
        self._create_connections()

    def _create_widgets(self):
        self.logging_grp = QtWidgets.QGroupBox("Logging")
        self.logging_level_field = QtWidgets.QComboBox()
        self.logging_level_field.addItems(["NOT SET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

        self.testing_grp = QtWidgets.QGroupBox("Testing")
        self.testing_temp_dir = shared_widgets.PathWidget(dialog_label="Set temp dir for Luna tests", label_text="Temp dir: ")
        self.testing_buffer_output_cb = QtWidgets.QCheckBox("Buffer output")
        self.testing_new_file_cb = QtWidgets.QCheckBox("New scene per test")
        self.testing_delete_files_cb = QtWidgets.QCheckBox("Delete test files")
        self.testing_delete_dirs_cb = QtWidgets.QCheckBox("Delete test dirs")

    def _create_layous(self):
        logging_layout = QtWidgets.QFormLayout()
        self.logging_grp.setLayout(logging_layout)
        logging_layout.addRow("Level: ", self.logging_level_field)

        testing_layout = QtWidgets.QVBoxLayout()
        self.testing_grp.setLayout(testing_layout)
        testing_layout.addWidget(self.testing_temp_dir)
        testing_layout.addWidget(self.testing_buffer_output_cb)
        testing_layout.addWidget(self.testing_new_file_cb)
        testing_layout.addWidget(self.testing_delete_files_cb)
        testing_layout.addWidget(self.testing_delete_dirs_cb)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.logging_grp)
        self.main_layout.addWidget(self.testing_grp)
        self.main_layout.addStretch()

    def _create_connections(self):
        pass

    def load_config(self):
        Logger.debug("Developer page:: loading config...")
        config_dict = Config.load()  # type:dict
        # Logging
        self.logging_level_field.setCurrentText(Logger.get_level(name=1))

        # Testing
        self.testing_temp_dir.line_edit.setText(config_dict.get(TestVars.temp_dir))
        self.testing_buffer_output_cb.setChecked(config_dict.get(TestVars.buffer_output))
        self.testing_new_file_cb.setChecked(config_dict.get(TestVars.new_file))
        self.testing_delete_files_cb.setChecked(config_dict.get(TestVars.delete_files))
        self.testing_delete_dirs_cb.setChecked(config_dict.get(TestVars.delete_dirs))

    def save_config(self):
        Logger.debug("Developer page:: saving config....")
        new_config = {}
        # Logging
        Logger.set_level(self.logging_level_field.currentText())
        new_config[LunaVars.logging_level] = Logger.get_level()

        # Testing
        new_config[TestVars.temp_dir] = self.testing_temp_dir.line_edit.text()
        new_config[TestVars.buffer_output] = self.testing_buffer_output_cb.isChecked()
        new_config[TestVars.new_file] = self.testing_new_file_cb.isChecked()
        new_config[TestVars.delete_files] = self.testing_delete_files_cb.isChecked()
        new_config[TestVars.delete_dirs] = self.testing_delete_dirs_cb.isChecked()

        # Update config
        Config.update(new_config)
        Logger.debug("Developer page :: saved config: {0}".format(new_config))
