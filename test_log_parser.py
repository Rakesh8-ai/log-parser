import subprocess
import unittest

class TestLogParser(unittest.TestCase):

    def run_cli(self, *args):
        result = subprocess.run(['python3', 'util.py', *args], capture_output=True, text=True)
        return result.stdout

    def test_help(self):
        output = self.run_cli('--help')
        self.assertIn("usage:", output.lower())  # Check for 'usage' in lowercase
        self.assertIn("-h", output)  # Check if the help option '-h' is listed
        self.assertIn("-f", output)  # Check if the '-f' option is listed
        self.assertIn("-l", output)  # Check if the '-l' option is listed
        self.assertIn("-t", output)  # Check if the '-t' option is listed

    def test_first(self):
        output = self.run_cli('--first', '5', 'test.log')
        self.assertEqual(len(output.splitlines()), 5)

    def test_last(self):
        output = self.run_cli('--last', '5', 'test.log')
        self.assertEqual(len(output.splitlines()), 5)

    def test_timestamps(self):
        output = self.run_cli('--timestamps', 'test.log')
        self.assertIn('14:55:12', output)
        self.assertIn('14:55:13', output)
        self.assertIn('14:55:14', output)
        self.assertIn('14:55:15', output)

    def test_ipv4(self):
        output = self.run_cli('--ipv4', 'test.log')
        self.assertIn('192.168.1.1', output)

    def test_ipv6(self):
        output = self.run_cli('--ipv6', 'test.log')
        self.assertIn('2001:0db8:85a3:0000:0000:8a2e:0370:7334', output)

if __name__ == '__main__':
    unittest.main()
