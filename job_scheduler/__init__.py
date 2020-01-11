# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin):
    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="https://en.wikipedia.org/wiki/Hello_world")

def get_implementation_class():
	return JobSchedulerPlugin()


__plugin_name__ = "Job-Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {
	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
	"octoprint.server.http.routes": __plugin_implementation__.route_hook
}
