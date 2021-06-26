# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import senaite.initializer


class SenaiteInitializerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=senaite.initializer)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'senaite.initializer:default')


SENAITE_INITIALIZER_FIXTURE = SenaiteInitializerLayer()


SENAITE_INITIALIZER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SENAITE_INITIALIZER_FIXTURE,),
    name='SenaiteInitializerLayer:IntegrationTesting',
)


SENAITE_INITIALIZER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SENAITE_INITIALIZER_FIXTURE,),
    name='SenaiteInitializerLayer:FunctionalTesting',
)


SENAITE_INITIALIZER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SENAITE_INITIALIZER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='SenaiteInitializerLayer:AcceptanceTesting',
)
