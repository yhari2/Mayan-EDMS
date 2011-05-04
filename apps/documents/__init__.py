from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from main.api import register_diagnostic, register_tool
from permissions.api import register_permissions

from documents.models import Document, DocumentPage, DocumentPageTransformation
from documents.staging import StagingFile
from documents.conf.settings import ENABLE_SINGLE_DOCUMENT_UPLOAD

PERMISSION_DOCUMENT_CREATE = 'document_create'
PERMISSION_DOCUMENT_PROPERTIES_EDIT = 'document_properties_edit'
PERMISSION_DOCUMENT_EDIT = 'document_edit'
PERMISSION_DOCUMENT_METADATA_EDIT = 'document_metadata_edit'
PERMISSION_DOCUMENT_VIEW = 'document_view'
PERMISSION_DOCUMENT_DELETE = 'document_delete'
PERMISSION_DOCUMENT_DOWNLOAD = 'document_download'
PERMISSION_DOCUMENT_TRANSFORM = 'document_transform'
PERMISSION_DOCUMENT_TOOLS = 'document_tools'

register_permissions('documents', [
    {'name': PERMISSION_DOCUMENT_CREATE, 'label': _(u'Create document')},
    {'name': PERMISSION_DOCUMENT_PROPERTIES_EDIT, 'label': _(u'Edit document properties')},
    {'name': PERMISSION_DOCUMENT_EDIT, 'label': _(u'Edit document')},
    {'name': PERMISSION_DOCUMENT_METADATA_EDIT, 'label': _(u'Edit document metadata')},
    {'name': PERMISSION_DOCUMENT_VIEW, 'label': _(u'View document')},
    {'name': PERMISSION_DOCUMENT_DELETE, 'label': _(u'Delete document')},
    {'name': PERMISSION_DOCUMENT_DOWNLOAD, 'label': _(u'Download document')},
    {'name': PERMISSION_DOCUMENT_TRANSFORM, 'label': _(u'Transform document')},
    {'name': PERMISSION_DOCUMENT_TOOLS, 'label': _(u'Execute document modifying tools')},
])

document_list = {'text': _(u'documents list'), 'view': 'document_list', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_list_recent = {'text': _(u'recent documents list'), 'view': 'document_list_recent', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_create = {'text': _(u'upload a new document'), 'view': 'document_create', 'famfam': 'page_add', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}
document_create_multiple = {'text': _(u'upload multiple new documents'), 'view': 'document_create_multiple', 'famfam': 'page_add', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}
document_create_sibling = {'text': _(u'upload new document using same metadata'), 'view': 'document_create_sibling', 'args': 'object.id', 'famfam': 'page_copy', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}
document_view = {'text': _(u'details (advanced)'), 'view': 'document_view', 'args': 'object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_view_simple = {'text': _(u'details (simple)'), 'view': 'document_view_simple', 'args': 'object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_delete = {'text': _(u'delete'), 'view': 'document_delete', 'args': 'object.id', 'famfam': 'page_delete', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DELETE]}}
document_multiple_delete = {'text': _(u'delete'), 'view': 'document_multiple_delete', 'famfam': 'page_delete', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DELETE]}}
document_edit = {'text': _(u'edit'), 'view': 'document_edit', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}}
document_edit_metadata = {'text': _(u'edit metadata'), 'view': 'document_edit_metadata', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_METADATA_EDIT]}}
document_multiple_edit_metadata = {'text': _(u'edit metadata'), 'view': 'document_multiple_edit_metadata', 'famfam': 'page_edit', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_METADATA_EDIT]}}
document_preview = {'text': _(u'preview'), 'class': 'fancybox', 'view': 'document_preview', 'args': 'object.id', 'famfam': 'magnifier', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_download = {'text': _(u'download'), 'view': 'document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}}
document_find_duplicates = {'text': _(u'find duplicates'), 'view': 'document_find_duplicates', 'args': 'object.id', 'famfam': 'page_refresh', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_find_all_duplicates = {'text': _(u'find all duplicates'), 'view': 'document_find_all_duplicates', 'famfam': 'page_refresh', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}, 'description': _(u'Search all the documents\' checksums and return a list of the exact matches.')}
document_clear_transformations = {'text': _(u'clear all transformations'), 'view': 'document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
document_multiple_clear_transformations = {'text': _(u'clear all transformations'), 'view': 'document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}

document_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'object.id', 'famfam': 'pencil_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_create = {'text': _(u'create new transformation'), 'class': 'no-parent-history', 'view': 'document_page_transformation_create', 'args': 'object.id', 'famfam': 'pencil_add', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_edit = {'text': _(u'edit'), 'class': 'no-parent-history', 'view': 'document_page_transformation_edit', 'args': 'object.id', 'famfam': 'pencil_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_delete = {'text': _(u'delete'), 'class': 'no-parent-history', 'view': 'document_page_transformation_delete', 'args': 'object.id', 'famfam': 'pencil_delete', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_page_view = {'text': _(u'page details'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'object.document_page.id', 'famfam': 'page_white', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_transformation_page_edit = {'text': _(u'edit page'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'object.document_page.id', 'famfam': 'page_white', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_EDIT]}}
document_page_transformation_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'object.document_page.id', 'famfam': 'pencil_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}

document_page_view = {'text': _(u'page image'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'object.id', 'famfam': 'page_white', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_text = {'text': _(u'page text'), 'class': 'no-parent-history', 'view': 'document_page_text', 'args': 'object.id', 'famfam': 'page_white', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_edit = {'text': _(u'edit page text'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'object.id', 'famfam': 'page_white', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_EDIT]}}
document_page_navigation_next = {'text': _(u'next page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_next', 'args': 'object.id', 'famfam': 'resultset_next', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_navigation_previous = {'text': _(u'previous page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_previous', 'args': 'object.id', 'famfam': 'resultset_previous', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_navigation_first = {'text': _(u'first page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_first', 'args': 'object.id', 'famfam': 'resultset_first', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_navigation_last = {'text': _(u'last page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_last', 'args': 'object.id', 'famfam': 'resultset_last', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_zoom_in = {'text': _(u'zoom in'), 'class': 'no-parent-history', 'view': 'document_page_zoom_in', 'args': 'object.id', 'famfam': 'zoom_in', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_zoom_out = {'text': _(u'zoom out'), 'class': 'no-parent-history', 'view': 'document_page_zoom_out', 'args': 'object.id', 'famfam': 'zoom_out', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_rotate_right = {'text': _(u'rotate right'), 'class': 'no-parent-history', 'view': 'document_page_rotate_right', 'args': 'object.id', 'famfam': 'arrow_turn_right', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_page_rotate_left = {'text': _(u'rotate left'), 'class': 'no-parent-history', 'view': 'document_page_rotate_left', 'args': 'object.id', 'famfam': 'arrow_turn_left', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}

document_missing_list = {'text': _(u'Find missing document files'), 'view': 'document_missing_list', 'famfam': 'folder_page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}

metadata_group_link = {'text': _(u'group actions'), 'view': 'metadatagroup_view', 'famfam': 'page_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
metadata_group_back_to_document = {'text': _(u'return to document'), 'view': 'document_view_simple', 'args': 'ref_object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
metadata_group_create_sibling = {'text': _(u'upload new document using same metadata'), 'view': 'document_create_sibling', 'args': 'ref_object.id', 'famfam': 'page_copy', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': 'object.id', 'famfam': 'drive_magnify'}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': 'object.id', 'famfam': 'drive_delete'}

register_links(Document, [document_view_simple, document_view, document_edit, document_edit_metadata, document_delete, document_download, document_find_duplicates, document_clear_transformations])
register_links(Document, [document_create_sibling], menu_name='sidebar')

register_multi_item_links(['metadatagroup_view', 'document_list', 'document_list_recent'], [document_multiple_clear_transformations, document_multiple_edit_metadata, document_multiple_delete])

if ENABLE_SINGLE_DOCUMENT_UPLOAD:
    register_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list_recent, document_list, document_create, document_create_multiple], menu_name='sidebar')
else:
    register_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list_recent, document_list, document_create_multiple], menu_name='sidebar')

register_links(DocumentPage, [
    document_page_transformation_list, document_page_view,
    document_page_text, document_page_edit,
])

register_links(DocumentPage, [
    document_page_navigation_first, document_page_navigation_previous,
    document_page_navigation_next, document_page_navigation_last
], menu_name='sidebar')

register_links(['document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out], menu_name='form_header')

register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
register_links(DocumentPageTransformation, [document_page_transformation_page_edit, document_page_transformation_page_view], menu_name='sidebar')
register_links('document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
register_links('document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
register_links(['document_page_transformation_edit', 'document_page_transformation_delete'], [document_page_transformation_page_transformation_list], menu_name='sidebar')

register_links(StagingFile, [staging_file_preview, staging_file_delete])

register_links(['metadatagroup_view'], [metadata_group_back_to_document, metadata_group_create_sibling], menu_name='sidebar')

register_diagnostic('documents', _(u'Documents'), document_missing_list)

register_tool(document_find_all_duplicates, namespace='documents', title=_(u'documents'))

def document_exists(document):
    try:
        if document.exists():
            return u'<span class="famfam active famfam-tick"></span>'
        else:
            return u'<span class="famfam active famfam-cross"></span>'
    except Exception, exc:
        return exc

register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            lambda x: u'<a class="fancybox" href="%(url)s"><img class="lazy-load" data-href="%(thumbnail)s" src="%(media_url)s/images/ajax-loader.gif" alt="%(string)s" /><noscript><img src="%(thumbnail)s" alt="%(string)s" /></noscript></a>' % {
                'url': reverse('document_preview', args=[x.pk]),
                'thumbnail': reverse('document_thumbnail', args=[x.pk]),
                'media_url': settings.MEDIA_URL,
                'string': _(u'thumbnail')
            }
        },
        {'name':_(u'metadata'), 'attribute':
            lambda x: x.get_metadata_string()
        },
    ])

if ENABLE_SINGLE_DOCUMENT_UPLOAD:
    register_menu([
        {'text': _(u'documents'), 'view': 'document_list_recent', 'links': [
            document_list_recent, document_list, document_create, \
            document_create_multiple
            
        ], 'famfam': 'page', 'position': 1}])
else:
    register_menu([
        {'text': _(u'documents'), 'view': 'document_list_recent', 'links': [
            document_list_recent, document_list, document_create_multiple
        ], 'famfam': 'page', 'position': 1}])
