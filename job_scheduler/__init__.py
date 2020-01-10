# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class OctoprintJobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin):
    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="https://en.wikipedia.org/wiki/Hello_world")

__plugin_name__ = "Job-Scheduler"
__plugin_implementation__ = OctoprintJobSchedulerPlugin()
