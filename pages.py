from PySide2 import QtWidgets
from Luna import Logger
from Luna import Config
from Luna import LunaVars
from Luna import TestVars
from Luna import HudVars
from Luna.interface import shared_widgets
from Luna.interface import hud
reload(shared_widgets)


class PageWidget(QtWidgets.QWidget):
    def __init__(self, config_dict, parent=None, category_name="Category"):
        super(PageWidget, self).__init__(parent)
        self.category_name = category_name
        self.config_dict = config_dict  # type: dict

    def load_config(self):
        raise NotImplementedError

    def save_config(self):
        raise NotImplementedError


class DeveloperPage(PageWidget):
    def __init__(self, config_dict, parent=None, category_name="Developer"):
        super(DeveloperPage, self).__init__(config_dict, parent=parent, category_name=category_name)

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

        self.misc_grp = QtWidgets.QGroupBox("Misc")
        self.misc_pyport_field = QtWidgets.QSpinBox()
        self.misc_pyport_field.setMinimum(1024)
        self.misc_pyport_field.setMaximum(49151)

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

        misc_layout = QtWidgets.QFormLayout()
        self.misc_grp.setLayout(misc_layout)
        misc_layout.addRow("Python port: ", self.misc_pyport_field)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.logging_grp)
        self.main_layout.addWidget(self.testing_grp)
        self.main_layout.addWidget(self.misc_grp)
        self.main_layout.addStretch()

    def _create_connections(self):
        pass

    def load_config(self):
        Logger.debug("Developer page - loading config...")

        # Logging
        Logger.set_level(self.config_dict.get(LunaVars.logging_level))
        self.logging_level_field.setCurrentText(Logger.get_level(name=1))

        # Testing
        self.testing_temp_dir.line_edit.setText(self.config_dict.get(TestVars.temp_dir))
        self.testing_buffer_output_cb.setChecked(self.config_dict.get(TestVars.buffer_output))
        self.testing_new_file_cb.setChecked(self.config_dict.get(TestVars.new_file))
        self.testing_delete_files_cb.setChecked(self.config_dict.get(TestVars.delete_files))
        self.testing_delete_dirs_cb.setChecked(self.config_dict.get(TestVars.delete_dirs))

        # Misc
        self.misc_pyport_field.setValue(self.config_dict.get(LunaVars.command_port))

    def save_config(self):
        Logger.debug("Developer page - saving config...")
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

        # Misc
        new_config[LunaVars.command_port] = self.misc_pyport_field.value()

        # Update config
        Config.update(new_config)
        Logger.debug("Developer page - saved config: {0}".format(new_config))


class OtherPage(PageWidget):
    def __init__(self, config_dict, parent=None, category_name="Other"):
        super(OtherPage, self).__init__(config_dict, parent=parent, category_name=category_name)

        self._create_widgets()
        self._create_layous()
        self._create_connections()

    def _create_widgets(self):
        self.hud_grp = QtWidgets.QGroupBox("HUD")
        self.hud_section_field = QtWidgets.QSpinBox()
        self.hud_block_field = QtWidgets.QSpinBox()
        self.hud_section_field.setMinimum(0)
        self.hud_section_field.setMaximum(9)

    def _create_layous(self):
        hud_layout = QtWidgets.QFormLayout()
        hud_layout.addRow("Block:", self.hud_block_field)
        hud_layout.addRow("Section:", self.hud_section_field)
        self.hud_grp.setLayout(hud_layout)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.hud_grp)
        self.setLayout(self.main_layout)

    def _create_connections(self):
        pass

    def load_config(self):
        Logger.debug("Other page - loading config...")
        # HUD
        self.hud_section_field.setValue(self.config_dict.get(HudVars.section))
        self.hud_block_field.setValue(self.config_dict.get(HudVars.block))

    def save_config(self):
        Logger.debug("Other page - saving config...")
        new_config = {}

        # HUD
        new_config[HudVars.section] = self.hud_section_field.value()
        new_config[HudVars.block] = self.hud_block_field.value()

        Config.update(new_config)
        Logger.debug("Other page - saved config: {0}".format(new_config))
        # Hud recreate
        Logger.info("Updating HUD...")
        hud.LunaHUD.create()
