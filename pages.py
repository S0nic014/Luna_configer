from PySide2 import QtWidgets
import luna
from luna import Logger
from luna import Config
from luna.interface import shared_widgets
from luna.interface import hud
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
        self.testing_temp_dir = shared_widgets.PathWidget(dialog_label="Set temp dir for luna tests", label_text="Temp dir: ")
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
        config_dict = Config.load()

        # Logging
        Logger.set_level(config_dict.get(luna.LunaVars.logging_level))
        self.logging_level_field.setCurrentText(Logger.get_level(name=1))

        # Testing
        self.testing_temp_dir.line_edit.setText(config_dict.get(luna.TestVars.temp_dir))
        self.testing_buffer_output_cb.setChecked(config_dict.get(luna.TestVars.buffer_output))
        self.testing_new_file_cb.setChecked(config_dict.get(luna.TestVars.new_file))
        self.testing_delete_files_cb.setChecked(config_dict.get(luna.TestVars.delete_files))
        self.testing_delete_dirs_cb.setChecked(config_dict.get(luna.TestVars.delete_dirs))

        # Misc
        self.misc_pyport_field.setValue(config_dict.get(luna.LunaVars.command_port))

    def save_config(self):
        Logger.debug("Developer page - saving config...")
        new_config = {}
        # Logging
        Logger.set_level(self.logging_level_field.currentText())
        new_config[luna.LunaVars.logging_level] = Logger.get_level()

        # Testing
        new_config[luna.TestVars.temp_dir] = self.testing_temp_dir.line_edit.text()
        new_config[luna.TestVars.buffer_output] = self.testing_buffer_output_cb.isChecked()
        new_config[luna.TestVars.new_file] = self.testing_new_file_cb.isChecked()
        new_config[luna.TestVars.delete_files] = self.testing_delete_files_cb.isChecked()
        new_config[luna.TestVars.delete_dirs] = self.testing_delete_dirs_cb.isChecked()

        # Misc
        new_config[luna.LunaVars.command_port] = self.misc_pyport_field.value()

        # Update config
        Config.update(new_config)
        Logger.debug("Developer page - saved config: {0}".format(new_config))


class OtherPage(PageWidget):
    def __init__(self, parent=None, category_name="Other"):
        super(OtherPage, self).__init__(parent=parent, category_name=category_name)

        self._create_widgets()
        self._create_layous()
        self._create_connections()

    def _create_widgets(self):
        # HUD
        self.hud_grp = QtWidgets.QGroupBox("HUD")
        self.hud_section_field = QtWidgets.QSpinBox()
        self.hud_block_field = QtWidgets.QSpinBox()
        self.hud_section_field.setMinimum(0)
        self.hud_section_field.setMaximum(9)
        # Unreal
        self.unreal_grp = QtWidgets.QGroupBox("Unreal Engine")
        self.unreal_project = shared_widgets.PathWidget(label_text="Project path:", dialog_label="Set Unreal project")

    def _create_layous(self):
        hud_layout = QtWidgets.QFormLayout()
        hud_layout.addRow("Block:", self.hud_block_field)
        hud_layout.addRow("Section:", self.hud_section_field)
        self.hud_grp.setLayout(hud_layout)

        unreal_layout = QtWidgets.QVBoxLayout()
        unreal_layout.addWidget(self.unreal_project)
        self.unreal_grp.setLayout(unreal_layout)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.hud_grp)
        self.main_layout.addWidget(self.unreal_grp)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def _create_connections(self):
        pass

    def load_config(self):
        Logger.debug("Other page - loading config...")
        config_dict = Config.load()
        # HUD
        self.hud_section_field.setValue(config_dict.get(luna.HudVars.section))
        self.hud_block_field.setValue(config_dict.get(luna.HudVars.block))
        self.unreal_project.line_edit.setText(config_dict.get(luna.UnrealVars.project, ""))

    def save_config(self):
        Logger.debug("Other page - saving config...")
        new_config = {}

        # HUD
        new_config[luna.HudVars.section] = self.hud_section_field.value()
        new_config[luna.HudVars.block] = self.hud_block_field.value()
        new_config[luna.UnrealVars.project] = self.unreal_project.line_edit.text()

        Config.update(new_config)
        Logger.debug("Other page - saved config: {0}".format(new_config))
        # Hud recreate
        Logger.info("Updating HUD...")
        hud.LunaHUD.create()
