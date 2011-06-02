import magic

from dms_plugins.pluginpoints import BeforeStoragePluginPoint
from dms_plugins.workers import Plugin, PluginError

MIMETYPES = [
                ('application/pdf', 'pdf'),
                ('image/tiff', 'tiff'),
                ('image/jpeg', 'jpg'),
                ('image/gif', 'gif'),
                ('image/png', 'png'),
                ('text/plain', 'txt'),
                ('application/msword', 'doc'),
                ('application/vnd.ms-excel', 'xls'),
            ]

def get_mimetypes():
    return [ x[0] for x in MIMETYPES ]

class FileTypeValidationPlugin(Plugin, BeforeStoragePluginPoint):
    title = "File Type Validator"
    description = "Validates document type against supported types"

    mimetypes = get_mimetypes()

    def work(self, request, document, **kwargs):
        filebuffer = document.get_file_obj()
        if filebuffer is None:
            raise PluginError('File buffer not initialized')
        mime = magic.Magic( mime = True )
        content = ''
        for line in filebuffer:
            content += line
        typ = mime.from_buffer( content )
        if not typ in self.mimetypes:
            raise PluginError('File type %s is not supported' % typ)
        document.set_mimetype(typ)
        return document
