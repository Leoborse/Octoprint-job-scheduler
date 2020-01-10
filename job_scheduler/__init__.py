# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class OctoprintJobSchedulerPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        self._logger.info("Job-Scheduler!")

__plugin_name__ = "Job-Scheduler"
__plugin_version__ = "1.0.0"
__plugin_description__ = "A job scheduler for OctoPrint"
__plugin_implementation__ = OctoprintJobSchedulerPlugin()
__plugin_author__ = "Leonardo Borselli"
__plugin_url__ = "https://https://github.com/Leoborse/Octoprint-job-scheduler"
