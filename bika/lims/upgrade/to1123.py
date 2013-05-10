from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from bika.lims.permissions import *

class Empty:
    pass

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    setup = portal.portal_setup

    # update affected tools
    setup.runImportStepFromProfile('profile-bika.lims:default', 'typeinfo')
    setup.runImportStepFromProfile('profile-bika.lims:default', 'workflow')
    setup.runImportStepFromProfile('profile-bika.lims:default', 'factorytool')
    setup.runImportStepFromProfile('profile-bika.lims:default', 'jsregistry')
    setup.runImportStepFromProfile('profile-bika.lims:default',
                                   'propertiestool')
    setup.runImportStepFromProfile('profile-bika.lims:default',
                                   'plone.app.registry')

    # Changes to the catalogs
    # create lexicon
    wordSplitter = Empty()
    wordSplitter.group = 'Word Splitter'
    wordSplitter.name = 'Unicode Whitespace splitter'
    caseNormalizer = Empty()
    caseNormalizer.group = 'Case Normalizer'
    caseNormalizer.name = 'Unicode Case Normalizer'
    stopWords = Empty()
    stopWords.group = 'Stop Words'
    stopWords.name = 'Remove listed and single char words'
    zc_extras = Empty()
    zc_extras.index_type = 'Okapi BM25 Rank'
    zc_extras.lexicon_id = 'Lexicon'

    # then add indexes
    bc = getToolByName(portal, 'bika_catalog')
    bc.addIndex('getContactTitle', 'FieldIndex')
    bc.addIndex('getClientTitle', 'FieldIndex')
    bc.addIndex('getProfileTitle', 'FieldIndex')
    bc.addIndex('getAnalysisCategory', 'KeywordIndex')
    bc.addIndex('getAnalysisService', 'KeywordIndex')
    bc.addIndex('getAnalysts', 'KeywordIndex')
    bc.addColumn('created')
    bc.addColumn('Creator')
    bc.addColumn('getAnalysts')
    bc.addColumn('getSampleID')
    bc.addColumn('getRequestID')
    bc.addColumn('getContactTitle')
    bc.addColumn('getClientTitle')
    bc.addColumn('getProfileTitle')
    bc.addColumn('getAnalysisCategory')
    bc.addColumn('getAnalysisService')
    bc.addColumn('getSamplePointTitle')
    bc.addColumn('getSampleTypeTitle')
    bc.addColumn('getDatePublished')
    bc.addColumn('getDateReceived')
    bc.addColumn('getDateSampled')
    bc.clearFindAndRebuild()

    # AnalysisRequestQuery and QueryFolder (listed in portal_tabs already)
    portal_properties = getToolByName(portal, 'portal_properties')
    ntp = getattr(portal_properties, 'navtree_properties')
    types = list(ntp.getProperty('metaTypesNotToList'))
    types.append("AnalysisRequestQuery")
    types.append("QueryFolder")
    ntp.manage_changeProperties(MetaTypesNotToQuery=types)

    mp = portal.queries.manage_permission
    mp(AddQuery, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 0)

    return True
