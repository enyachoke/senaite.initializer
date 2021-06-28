# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from ftw.oidcauth.plugin import OIDCPlugin
from zope.component.hooks import getSite
from App.config import getConfiguration
import os
import json
from pathlib import Path
from Products.CMFCore.utils import getToolByName
from pprint import pprint
import tarfile
import io


DEFAULT_ID_OIDC = 'oidc'
TITLE_OIDC = 'Open ID connect'

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'senaite.initializer:uninstall',
        ]


def _add_oidc(pas, pluginid, title):
    if pluginid in pas.objectIds():
        return title + ' already installed.'
    plugin = OIDCPlugin(pluginid, title=title)
    config_file = os.path.join(os.path.dirname(getConfiguration().clienthome),'','oidc','client.json')
    if Path(config_file).exists():
        f = open(config_file)
        config = json.load(f)
        for key in config:
            value = config[key]
            if key=='properties_mapping':
                value = json.dumps(config[key])
            plugin._setPropValue(key, value)
        f.close()
        
    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info['interface']
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface,
            [x[0] for x in pas.plugins.listPlugins(interface)[:-1]],
        )

def _load_senaite_data(context):
    portal_setup = getToolByName(context, 'portal_setup')
    tar_file_path =  os.path.join(os.path.dirname(getConfiguration().clienthome),'','importdata','data.tar.gz')
    if Path(tar_file_path).exists():
        tar_fileobj = io.BytesIO()
        with open(tar_file_path, 'r:*') as fin:
            tar_fileobj = io.BytesIO(fin.read())
        tarball = tar_fileobj.getvalue()
        result = portal_setup.runAllImportStepsFromProfile(None, True, archive=tarball)
        steps_run = 'Steps run: %s' % ', '.join(result['steps'])
        portal_setup.manage_importSteps(manage_tabs_message=steps_run,
                                        messages=result['messages'])

def _remove_plugin(pas, pluginid):
    if pluginid in pas.objectIds():
        pas.manage_delObjects([pluginid])


def post_install(context):
    """Post install script"""
    aclu = getSite().acl_users
    _add_oidc(aclu, DEFAULT_ID_OIDC, TITLE_OIDC)
    _load_senaite_data(context)

def uninstall(context):
    """Uninstall script"""
    aclu = getSite().acl_users
    _remove_plugin(aclu, DEFAULT_ID_OIDC)
