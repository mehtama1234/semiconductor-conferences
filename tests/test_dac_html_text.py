from scripts.collect_dac_paper_evidence import clean


def test_numeric_inequality_does_not_swallow_description():
    assert clean('CNN (<13k parameters), at 64nJ/frame.<br>Next.') == 'CNN (<13k parameters), at 64nJ/frame. Next.'
    assert clean('x &lt; 3 and y &gt; 2') == 'x < 3 and y > 2'
    assert clean('<b>Power</b>: 11μW<!-- hidden -->') == 'Power: 11μW'
