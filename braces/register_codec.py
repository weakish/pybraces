import codecs, cStringIO, encodings, tokenize
import traceback
from encodings import utf_8

class BracesStreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)

        self._tokens = []
        self._indent = 0
        tokenize.tokenize(self.stream.readline, self._handle_token)
        data = tokenize.untokenize(self._tokens)

        self.stream = cStringIO.StringIO(data)

    def _handle_token(self, tok_type, tok_str, start_pos, end_pos, lineno):
        # Ignore indenting
        if tok_type in (tokenize.INDENT, tokenize.DEDENT):
            return
        # Ignore `:`
        if tok_type == tokenize.OP and tok_str == ':':
            return

        if tok_type == tokenize.COMMENT:
            if tok_str == '#{' or tok_str == '# {':
                tok_type = tokenize.INDENT
                self._indent += 1
                tok_str = '  ' * self._indent
                self._tokens.append((tokenize.COLON, ':'))
            elif tok_str == '#}' or tok_str == '# }':
                tok_type = tokenize.DEDENT
                self._indent -= 1

        self._tokens.append((tok_type, tok_str))

def search_function(encoding):
    if encoding != 'braces': return None
    # Assume utf8 encoding
    utf8 = encodings.search_function('utf8')
    return codecs.CodecInfo(
        name = 'braces',
        encode = utf8.encode,
        decode = utf8.decode,
        incrementalencoder = utf8.incrementalencoder,
        incrementaldecoder = utf8.incrementaldecoder,
        streamreader = BracesStreamReader,
        streamwriter = utf8.streamwriter)

codecs.register(search_function)
