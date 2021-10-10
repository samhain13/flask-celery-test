import os
import subprocess


class VirusScanner:
    '''
    A base class for passing on the scanning operations to the system via
    the subprocess module. Child classes must have their own implementation
    of evaluate_result.
    '''
    debug = False
    command_line = ''
    filepath = ''
    scan_result = ''

    def __init__(self, filepath, debug=False):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'{filepath} doesn\'t exist')
        self.filepath = filepath
        self.debug = debug
        self.begin_scan()

    def begin_scan(self):
        proc_list = self.command_line.replace(
            '{filepath}', self.filepath).split(' ')
        proc = subprocess.run(proc_list, capture_output=True)
        self.scan_result = proc.stdout

        if type(self.scan_result).__name__ == 'bytes':
            self.scan_result = self.scan_result.decode('utf-8')

        if self.debug:
            print('Scanned file:', self.filepath)
            print('Scan result:', self.scan_result)

    def evaluate_result(self):
        raise NotImplementedError


class ClamScan(VirusScanner):
    command_line = 'clamscan {filepath}'

    def evaluate_result(self):
        return self.scan_result.startswith('{}: OK'.format(self.filepath))
