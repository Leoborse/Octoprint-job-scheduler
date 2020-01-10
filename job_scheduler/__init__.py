# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class OctoprintJobSchedulerPlugin(
            octoprint.plugin.StartupPlugin,
            octoprint.plugin.TemplatePlugin
            ):
    def on_after_startup(self):
        self._logger.info("Job-Scheduler!")

__plugin_name__ = "Job-Scheduler"
__plugin_implementation__ = OctoprintJobSchedulerPlugin()
