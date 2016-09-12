import codecs
import encodings
import tokenize
from encodings import utf_8

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

class EndStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)

        self._tokens = []
        self._indent = 0
        tokenize.tokenize(self.stream.readline, self._handle_token)
        data = tokenize.untokenize(self._tokens)

        self.stream = StringIO(data)

    def _handle_token(self, tok_type, tok_str, start_pos, end_pos, lineno):
        # Ignore indenting
        if tok_type in (tokenize.INDENT, tokenize.DEDENT):
            return

        if tok_type == tokenize.OP and tok_str == ':':
            tok_type = tokenize.INDENT
            self._indent += 1
            tok_str = '  ' * self._indent
            self._tokens.append((tokenize.COLON, ':'))
        elif tok_type == tokenize.NAME and tok_str == 'end':
            tok_type = tokenize.DEDENT
            self._indent -= 1

        self._tokens.append((tok_type, tok_str))

def search_function(encoding):
    if encoding != 'end': return None
    # Assume utf8 encoding
    utf8 = encodings.search_function('utf8')
    return codecs.CodecInfo(
        name = 'end',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder = utf8.incrementalencoder,
        incrementaldecoder = utf8.incrementaldecoder,
        streamreader = EndStreamReader,
        streamwriter = utf8.streamwriter)

codecs.register(search_function)
