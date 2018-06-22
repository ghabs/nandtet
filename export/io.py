"""
Contains class for input output and cleaning of file. If initialized with a transform function, it will apply the transform
to every line and then write it out.
"""
class IoJack():
    def __init__(self, t=None):
        self.transform = t
    
    def _clean(self, line):
        "remove comments, white space, and split"
        if line[0] in ['','/','*']:
            return False
        return line.strip().split()

    def io(self, input_file, output_file):
        """
        Open a file and clean the line, and apply the transformation func.
        Transform func must take in a list.
        """
        with open(input_file, 'r') as i, open(output_file, 'w') as w:
            for line in i:
                line = self._clean(line)
                if not line:
                    continue
                if self.transform:
                    line = self.transform(line)
                w.write(line)
        return