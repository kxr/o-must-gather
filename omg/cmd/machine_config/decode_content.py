from urllib.parse import unquote
from base64 import b64decode
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def decode_content(content):
    """
    Decodes url/bas64 encoded content found in machine-configs
    Certificate data is also converted to human readable format
    """
    split = content.split(',', 1)
    head = split[0]
    data = split[1]
    if head.startswith('data:'):
        if len(data) == 0:
            return '' 
        form = head[5:].split(';')
        if 'base64' in form:
            charset = next((x[8:] for x in form if x[0:8] == 'charset='),'utf-8')
            dec_data = b64decode(data).decode(charset)
        else:
            dec_data = unquote(data)
        
        if dec_data.startswith('-----BEGIN CERTIFICATE-----'):
            certs = []
            cert = []
            for cert_line in dec_data.splitlines():
                if cert_line != '-----END CERTIFICATE-----':
                    cert.append(cert_line)
                else:
                    cert.append(cert_line)
                    certs.append( '\n'.join(cert) )
                    cert = []
            dec_certs = []
            for c in certs:
                dec_cert = []
                parse_cert = x509.load_pem_x509_certificate(str.encode(c), default_backend())
                dec_cert.append('~~~~~BEGIN CERTIFICATE~~~~~')
                dec_cert.append( 'SUBJECT    : ' + parse_cert.subject.rfc4514_string() )
                dec_cert.append( 'ISSUER     : ' + parse_cert.issuer.rfc4514_string() )
                dec_cert.append( 'SERIAL     : ' + str(parse_cert.serial_number) )
                dec_cert.append( 'NOT BEFORE : ' + parse_cert.not_valid_before.isoformat() )
                dec_cert.append( 'NOT AFTER  : ' + parse_cert.not_valid_after.isoformat() )
                dec_cert.append('~~~~~END CERTIFICATE~~~~~')
                dec_certs.append( '\n'.join(dec_cert))
            return '\n'.join(dec_certs)
        else:
            return dec_data
    else:
        print('[Warning] Unable to recognize content (not starting with "data:")')
        return content
