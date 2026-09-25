from datetime import date

from bridge import tester

OPT_XML = b"""<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
<Worksheet ss:Name="Tester Optimizator Results"><Table>
<Row><Cell><Data ss:Type="String">Pass</Data></Cell><Cell><Data ss:Type="String">Result</Data></Cell>
<Cell><Data ss:Type="String">InpChannel</Data></Cell></Row>
<Row><Cell><Data ss:Type="Number">3</Data></Cell><Cell><Data ss:Type="Number">12.5</Data></Cell>
<Cell><Data ss:Type="Number">20</Data></Cell></Row>
</Table></Worksheet></Workbook>"""


def test_ini_contains_account_and_inputs():
    job = tester.Job("QB\\QB_Donchian.ex5", "XAUUSD", "H1", date(2020, 1, 1), date(2024, 1, 1),
                     params={"InpChannel": tester.Param(20, 10, 5, 60), "InpSlAtr": tester.Param(2.0)},
                     optimisation="genetic", tag="abc", deposit=100, currency="GBP")
    ini = job.ini_text()
    assert "Deposit=100" in ini and "Currency=GBP" in ini and "Leverage=1:100" in ini
    assert "Optimization=2" in ini and "Model=1" in ini
    assert "InpChannel=20||10||5||60||Y" in ini and "InpSlAtr=2||2||0||2||N" in ini
    assert "InpRunTag=abc\r\n" in ini
    assert "Report=reports\\abc" in ini and "ShutdownTerminal=1" in ini


def test_parse_opt_xml(tmp_path):
    p = tmp_path / "r.xml"
    p.write_bytes(OPT_XML)
    rows = tester.parse_opt_xml(p)
    assert rows == [{"Pass": 3.0, "Result": 12.5, "InpChannel": 20.0}]


def test_parse_report_html(tmp_path):
    html = ("<html><body><table><tr><td>Total Net Profit:</td><td>123.45</td>"
            "<td>Profit Factor:</td><td>1.52</td></tr>"
            "<tr><td>Equity Drawdown Relative:</td><td>12.34% (25.00)</td></tr>"
            "<tr><td>Total Trades:</td><td>210</td></tr></table></body></html>")
    p = tmp_path / "r.htm"
    p.write_text(html, encoding="utf-16")
    s = tester.parse_report(p)
    assert s["net_profit"] == 123.45 and s["profit_factor"] == 1.52 and s["trades"] == 210


def test_every_ea_input_is_written_so_tester_cannot_reuse_stale_values():
    job = tester.Job(r"QB\QB_Rules.ex5", "XAUUSD", "H1", date(2024, 1, 1), date(2024, 2, 1),
                     params={"InpChannel": tester.Param(30)}, tag="t1", deposit=100, currency="USD")
    ini = job.ini_text()
    assert "InpChannel=30||30||0||30||N" in ini
    assert "InpFamily=0||0||0||0||N" in ini            # enum default resolved from Signals.mqh
    assert "InpBalanceScale=1||1||0||1||N" in ini       # from an included header
    assert "InpMlModel=\r\n" in ini and "InpRunTag=t1\r\n" in ini
