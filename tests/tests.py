from atparlpy import CommitteeReports, Inquiries, Parliamentarians
from atparlpy.parliamentarians import MemberOfParliament, MemberOfTheNationalCouncil

class TestCommitteeReports:
    def test_ctor_api(self):

        result = CommitteeReports(nrbr="NR", gp_code="XXVII").AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.gp_code == "XXVII" for c in result)

        result = CommitteeReports(nrbr="NR", gp=27).AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.gp_code == "XXVII" for c in result)

    def test_fluent_api(self):
        result = CommitteeReports().nrbr("NR").gp_code("XXVII").AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.gp_code == "XXVII" for c in result)

        result = CommitteeReports().nrbr("NR").gp(27).AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.gp_code == "XXVII" for c in result)

    def test_nr_br(self):
        result = Inquiries(gp=28, nrbr="BR").AsList()
        assert len(result) > 0
        assert all(c.nrbr == "BR" for c in result)

        result = Inquiries(gp=28, nrbr="NR").AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
    
    def test_filter(self):
        result = Inquiries(gp=28, nrbr="NR").themen("Arbeit").AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.themen and "Arbeit" in c.themen for c in result)

        result = Inquiries(gp=28, nrbr="NR").themen(["Arbeit", "Bildung"]).AsList()
        assert len(result) > 0
        assert all(c.nrbr == "NR" for c in result)
        assert all(c.themen and ("Arbeit" in c.themen or "Bildung" in c.themen) for c in result)
    
    def test_parliamentarians_nr_br(self):
        result = Parliamentarians(nrbr="NR").AsList()
        assert len(result) == 183
        assert all(type(p) == MemberOfParliament for p in result)

        result = Parliamentarians(nrbr="BR").AsList()
        assert len(result) == 60
        assert all(type(p) == MemberOfTheNationalCouncil for p in result)
