import unittest
from unittest.mock import Mock, call
from kauppa import Kauppa
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        self.tuotteet = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "leipa", 7),
            3: Tuote(3, "juusto", 4),
        }
        self.saldot = {1: 10, 2: 10, 3: 0}

        self.varasto_mock.saldo.side_effect = lambda tuote_id: self.saldot[tuote_id]
        self.varasto_mock.hae_tuote.side_effect = lambda tuote_id: self.tuotteet[tuote_id]

        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock,
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_maksettaessa_kaksi_erilaista_tuotetta_tilisiirto_on_oikea(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 12
        )

    def test_maksettaessa_kaksi_samaa_tuotetta_tilisiirto_on_oikea(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_maksettaessa_tuote_varastossa_ja_loppunut_tuote_tilisiirto_on_oikea(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_uusi_asiointi_nollaa_edellisen_ostoskoriin(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("arto", "54321")

        self.pankki_mock.tilisiirto.assert_called_with(
            "arto", 42, "54321", "33333-44455", 7
        )

    def test_viitenumero_pyydetaan_jokaiselle_maksutapahtumalle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("arto", "54321")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("maija", "98765")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

    def test_perakkaisten_maksujen_viitenumerot_ovat_jokaisella_uudet(self):
        self.viitegeneraattori_mock.uusi.side_effect = [101, 102, 103]

        for nimi, tilinumero, tuote_id in (
            ("pekka", "12345", 1),
            ("arto", "54321", 2),
            ("maija", "98765", 1),
        ):
            self.kauppa.aloita_asiointi()
            self.kauppa.lisaa_koriin(tuote_id)
            self.kauppa.tilimaksu(nimi, tilinumero)

        self.assertEqual(
            self.pankki_mock.tilisiirto.call_args_list,
            [
                call("pekka", 101, "12345", "33333-44455", 5),
                call("arto", 102, "54321", "33333-44455", 7),
                call("maija", 103, "98765", "33333-44455", 5),
            ],
        )

    def test_tuote_poistetaan_korista_ja_palautetaan_varastoon(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.varasto_mock.palauta_varastoon.assert_called_once_with(
            self.tuotteet[1]
        )
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 0
        )

    def test_tuotteen_vertailu_hashaus_ja_tekstiesitys(self):
        tuote1 = Tuote(1, "maito", 5)
        tuote1_kopio = Tuote(1, "maito", 5)
        eri_tuote = Tuote(2, "leipa", 7)

        self.assertEqual(tuote1, tuote1_kopio)
        self.assertNotEqual(tuote1, eri_tuote)
        self.assertEqual(hash(tuote1), hash(tuote1_kopio))
        self.assertEqual(str(tuote1), "maito")
