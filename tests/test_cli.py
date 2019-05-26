from nested_diff import cli


class Dumper(cli.Dumper):
    def encode(self, data):
        return data


def test_dumper_dump_default_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.dump(stringio_tty, 'text')

    assert 'text' == stringio_tty.getvalue()


def test_dumper_dump_default_without_tty(stringio):
    dumper = Dumper()
    dumper.dump(stringio, 'text')

    assert 'text' == stringio.getvalue()


def test_dumper_dump_final_new_line_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio_tty, 'text')

    assert 'text\n' == stringio_tty.getvalue()


def test_dumper_dump_final_new_line_without_tty(stringio):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio, 'text')

    assert 'text' == stringio.getvalue()
