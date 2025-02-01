import unittest
import tramdata
import json

TRAM_FILE = "./tramnetwork.json"
LINE_FILE = "./data/tramlines.txt"


class TestTramData(unittest.TestCase):
    def setUp(self):
        with open(TRAM_FILE, encoding="utf-8") as trams:
            tramdict = json.loads(trams.read())
            self.tramdict = tramdict
            self.stopdict = tramdict["stops"]
            self.linedict = tramdict["lines"]
            self.timedict = tramdict["times"]
            self.stopset = {
                stop for line in self.linedict for stop in self.linedict[line]
            }

            self.answers = {
                "time with 1 from Härlanda to Brunnsparken": 10,
                "time with 1 from Kaggeledstorget to Briljantgatan": 34,
                "time with 1 from Smaragdgatan to Opaltorget": 0,
                "time with 1 from Härlanda to Opaltorget": 32,
                "time with 1 from Östra Sjukhuset to Opaltorget": 38,
                "time with 1 from Östra Sjukhuset to Smaragdgatan": 38,
                "time with 1 from Östra Sjukhuset to Munkebäckstorget": 4,          
                "time with 1 from Munkebäckstorget to Centralstationen": 11,
                "time with 1 from Härlanda to Opaltorget": 32,
                "time with 2 from Elisedal to Vasaplatsen": 16,
                "time with 2 from Axel Dahlströms Torg to Lackarebäck": 34,
                "time with 2 from Mölndals Innerstad to Axel Dahlströms Torg": 37,
                "time with 2 from Mölndals sjukhus to Liseberg Södra": 10,
                "time with 2 from Lana to Olivedalsgatan": 24,
                "time with 2 from Axel Dahlströms Torg to Handelshögskolan": 11,
                "time with 2 from Botaniska Trädgården to Mölndals sjukhus": 32,
                "time with 3 from Järntorget to Hagakyrkan": 3,
                "time with 3 from Jaegerdorffsplatsen to Svingeln": 22,
                "time with 3 from Klintens Väg to Valand": 22,
                "time with 3 from Ostindiegatan to Redbergsplatsen": 28,
                "time with 3 from Virginsgatan to Marklandsgatan":42,
                "time with 3 from Klintens Väg to Godhemsgatan": 1,
                "time with 3 from Klintens Väg to Mariaplan": 3,
                "time with 3 from Klintens Väg to Centralstationen": 26,
                "time with 3 from Klintens Väg to Härlanda": 35,
                "time with 3 from Klintens Väg to Stockholmsgatan": 34,
                "time with 3 from Klintens Väg to Virginsgatan": 38,
                "time with 3 from Godhemsgatan to Härlanda": 34,
                "time with 4 from Gamlestads Torg to Lana": 20,
                "time with 4 from Mölndals Innerstad to Angered Centrum": 34,
                "time with 4 from Gamlestads Torg to Hammarkullen": 4,
                "time with 4 from Berzeliigatan to Kungsportsplatsen": 4,
                "time with 4 from Lackarebäck to Valand": 13,
                "time with 4 from Hjällbo to Berzeliigatan": 13,
                "time with 5 from Virginsgatan to Welandergatan": 2,
                "time with 5 from Sälöfjordsgatan to Östra Sjukhuset": 35,
                "time with 5 from Östra Sjukhuset to Varmfrontsgatan": 42,
                "time with 5 from Solrosgatan to Frihamnen": 21,
                "time with 5 from Vågmästareplatsen to Friskväderstorget": 11,
                "time with 5 from Eketrägatan to Önskevädersgatan": 5,
                "time with 6 from Linnéplatsen to Gropegårdsgatan": 19,
                "time with 6 from Allhelgonakyrkan to Medicinaregatan": 30,
                "time with 6 from Medicinaregatan to Gropegårdsgatan": 22,
                "time with 6 from Nymånegatan to Nordstan": 41,
                "time with 6 from Linnéplatsen to Friskväderstorget": 26,
                "time with 6 from Aprilgatan to Varmfrontsgatan": 63,
                "time with 6 from Aprilgatan to Kortedala Torg": 2,
                "time with 6 from Allhelgonakyrkan to Chalmers": 27,
                "time with 6 from Hagakyrkan to Vågmästareplatsen": 8,
                "time with 6 from Ullevi Norra to Prinsgatan": 17,
                "time with 6 from Hagakyrkan to Varmfrontsgatan": 22,
                "time with 7 from Komettorget to Galileis Gata": 4,
                "time with 7 from Teleskopgatan to Komettorget": 3,
                "time with 7 from Rymdtorget Spårvagn to Positivgatan": 45,
                "time with 7 from Komettorget to Nymånegatan": 10,
                "time with 7 from Komettorget to Opaltorget": 51,
                "time with 7 from Kortedala Torg to Kviberg": 5,
                "time with 7 from SKF to Kapellplatsen": 14,
                "time with 7 from Komettorget to Rymdtorget Spårvagn": 2,
                "time with 7 from Marklandsgatan to Opaltorget": 10,
                "time with 8 from Angered Centrum to Hjällbo": 7,
                "time with 8 from Gamlestads Torg to Medicinaregatan": 20,
                "time with 8 from Redbergsplatsen to Musikvägen": 28,
                "time with 8 from Angered Centrum to Svingeln": 15,
                "time with 8 from Angered Centrum to Frölunda Torg Spårvagn": 43,
                "time with 8 from Ullevi Södra to Nymilsgatan": 20,
                "time with 8 from Hjällbo to Storås": 4,
                "time with 8 from Musikvägen to Frölunda Torg Spårvagn": 3,
                "time with 9 from Storås to Kungssten": 31,
                "time with 9 from Hjällbo to Sandarna": 25,
                "time with 9 from Centralstationen to Gamlestads Torg": 6,
                "time with 9 from Storås to Sandarna": 29,
                "time with 9 from Centralstationen to Kungssten": 20,
                "time with 9 from Angered Centrum to Kungssten": 34,
                "time with 9 from Brunnsparken to Vagnhallen Majorna": 13,
                "time with 10 from Wavrinskys Plats to Väderilsgatan": 28,
                "time with 10 from Kapellplatsen to Frihamnen": 12,
                "time with 10 from Doktor Sydows Gata to Lilla Bommen": 13,
                "time with 10 from Doktor Sydows Gata to Lilla Bommen": 13,
                "time with 10 from Doktor Sydows Gata to Väderilsgatan": 31,
                "time with 10 from Frihamnen to Önskevädersgatan": 12,
                "time with 10 from Valand to Centralstationen": 4,
                "time with 11 from Hinsholmen to Järntorget": 22,
                "time with 11 from Saltholmen to Domkyrkan": 31,
                "time with 11 from SKF to Januarigatan": 10,
                "time with 11 from Käringberget to SKF": 35,
                "time with 11 from Långedrag to Masthuggstorget": 21,
                "time with 11 from Saltholmen to Kungssten": 10,
                "time with 11 from Saltholmen to Komettorget": 55,
                "time with 11 from Domkyrkan to Kortedala Torg": 17,
                "time with 11 from Sannaplan to Teleskopgatan": 39,
                "time with 11 from Ekedal to Runstavsgatan": 29,
                "time with 13 from Saltholmen to Hagen": 7,
                "time with 13 from Saltholmen to Centralstationen": 38,
                "time with 13 from Nya Varvsallén to Sandarna": 3,
                "time with 13 from Sandarna to Sahlgrenska Huvudentré": 12,
                "time with 13 from Sandarna to Chalmers": 17,
                "time with 13 from Mariaplan to Centralstationen": 24,
                "time with 13 from Sannaplan to Chalmers": 16,
                "time with 13 from Saltholmen to Centralstationen": 38,
                "time with 13 from Korsvägen to Långedrag": 30,
                
                #Testar via
                "via Lana": ['2' ,'4'],
                "via Östra Sjukhuset": ['1' ,'5'],
                "via Valand": ['3' ,'4', '5', '7', '10'],
                "via Stenpiren": ['1' ,'9'],
                "via Mariaplan": ['3' ,'11', '13'],
                "via Komettorget": ['7' ,'11'],
                "via Nordstan": ['6'],
                "via Svingeln": ['1' ,'3','6', '8'],
                "via Ullevi Södra": ['2' ,'6','8','13'],
                "via Sannaplan": ['9','11' ,'13'],
                "via Saltholmen": ['11' ,'13'],
                "via Eketrägatan": ['5' ,'6', '10'],
                "via Kapellplatsen": ['7' ,'10'],
                "via Järntorget": ['1' ,'3', '6', '9', '11'],
                "via Kviberg": ['6' ,'7', '11'],
                "via Lantmilsgatan": ['1' ,'7', '8'],
                "via Angered Centrum": ['4' ,'8', '9'],
                "via Hjällbo": ['4' ,'8', '9'],
                "via Brunnsparken": ['1' ,'2', '3','4','5','6','7','9','10','11'],
                "via SKF": ['6' ,'7', '11'],
                "via Grönsakstorget": ['2' ,'6', '11'],
                "via Fjällgatan": ['11'],
                "via Valand": ['3' ,'4', '5','7','10'],
                "via Chalmers": ['6' ,'7','8','10', '13'],
                "via Hagen": ['11', '13'],
                "via Hagakyrkan": ['3', '6', '11'],
                "via Ekedal": ['11'],
                "via Januarigatan": ['7', '11'],
                "via Vasaplatsen": ['2', '3','7','10'],
                "via Prinsgatan": ['1', '6'],
                "via Aprilgatan": ['6'],
                "via Vågmästareplatsen": ['5','6', '10'],
                "via Almedal": ['2', '4'],

                #Testar between
                "between Lana and Lackarebäck": ['2','4'],
                "between Tingvallsvägen and Östra Sjukhuset": ['1','5'],
                "between Klintens Väg and Mariaplan": ['3'],
                "between Domkyrkan and Brunnsparken": ['2','6','11'],
                "between Östra Sjukhuset and Brunnsparken": ['1','5'],
                "between Valand and Bögatan": ['5'],
                "between Elisedal and Storås": ['4'],
                "between Chalmers and Ejdergatan": ['6','8'],
                "between Järntorget and Stenpiren": ['1','9'],
                "between Chapmans Torg and Kungssten": ['9'],
                "between Svingeln and Redbergsplatsen": ['1','3','6','8'],
                "between Centralstationen and Brunnsparken": ['1','2','3','4', '7', '9', '10', '11'],

            
                #Testar felhantering
                "time with 6 from agakyrkan to Varmfrontsgatan": -1,
                "time with 25 from Komettorget to Nymånegatan": -1,
                "time with 7 from SK to Kapellplatsen": -1,
                "time with 24 from Lana to Chalmers": -1,
                "time with 8 from to Nymilsgatan": -1,
                "time with 8 from Musikvägen to ": -1,
                "time with 8 from Angered Centum to Svineln": -1,
                "between Korsvägen and Clamers":-1,
                "between Nymilsgaan and Lackarebäck": -1,
                "between Valad and Brunsparken": -1,
                "via Marplan": -1,
                "via ": -1,
                "via Nrdstan": -1,
                "via Vald": -1,
                "via Ötra Sjukhuset": -1,
                "time with 7 from Kortedala Torg t Kviberg": False,
                "time ith 7 from Marklandsgatan to Opaltorget": False,
                "ia Lana": False,
                "va Stenpiren": False,
                "" : False,
                '[]': False,
                '%' : False,
                "time with 2 from Angered Centrum to Svingeln": 'Angered Centrum and Svingeln are not along the same line!',
                "time with 2 from Lana to Chalmers": 'Lana and Chalmers are not along the same line!',
                "time with 5 from Lana to Chalmers": 'Lana and Chalmers are not along the same line!',
                "time with 10 from Östra Sjukhuset to Olskrokstorget": 'Östra Sjukhuset and Olskrokstorget are not along the same line!',
                "between Lana and Chalmers": [],
                "between Chalmers and Lana": [],
                "between Nymilsgatan and Lackarebäck": [],
                "between Komettorget and Lackarebäck": [],
              
               


            }


    def test_stops_exist(self):
        for stop in self.stopset:
            self.assertIn(stop, self.stopdict, msg=stop + " not in stopdict")

    #Tests that all tram lines listed in the original text file tramlines.txt are included in linedict
    def test_lines(self):
        lines_native = [
            tramdata.retrieve_data(LINE_FILE)[0][item] for item in tramdata.retrieve_data(LINE_FILE)[1]
        ]
        lines_dict = list(self.linedict.keys())
        self.assertEqual(lines_native, lines_dict)

    #Tests that list of stops for each tramline is the same in tramlines.txt and linedict
    def test_stops(self):
        source_data = [item[0] for item in tramdata.retrieve_data(LINE_FILE)[0]]
        lines_index = tramdata.retrieve_data(LINE_FILE)[1]
        n = 0
        for line in self.linedict:
            if n + 1 < len(lines_index):
                self.assertEqual(
                    self.linedict[line],
                    source_data[lines_index[n] + 1 : lines_index[n + 1]],
                )
                n += 1

    #Tests that all distances less than 20 km
    def test_distances(self):
        checked_stops = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                for other_stops in self.linedict[line][self.linedict[line].index(stop)+1:]:
                    if (stop,other_stops) not in checked_stops:
                    
                        self.assertLess(tramdata.distance_between_stops(self.stopdict, stop, other_stops),20,)
                        checked_stops.add((stop,other_stops))
                        checked_stops.add((other_stops,stop))

    #Tests that time from a to b is equal to time from b to a
    def test_timeCorrespondense(self):
        checked_stops = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                for other_stops in self.linedict[line][self.linedict[line].index(stop)+1:]:
                    if (stop,other_stops) not in checked_stops:
                        self.assertEqual(
                            tramdata.time_between_stops(
                                self.linedict, self.timedict, line, stop, other_stops
                            ),
                            tramdata.time_between_stops(
                                self.linedict, self.timedict, line, other_stops, stop
                            ),
                        )
                        checked_stops.add((stop,other_stops))
                        checked_stops.add((other_stops,stop))

    #Verifies that there's no redundancy in timesdict
    def test_duplicates(self):
        for stop in self.timedict:
            for sub_stop in list(self.timedict[stop].keys()):
                if sub_stop in self.timedict:
                    self.assertNotIn(stop, list(self.timedict[sub_stop].keys()))
   
    #Tests that timesdict contains all stops
    def test_times_exist(self):
        set1 = set()
        for stop in self.timedict:
            set1.add(stop)
            for element in list(self.timedict[stop].keys()):
                set1.add(element)

        self.assertEqual(set1, self.stopset)

    #Tests that timesdict include all possible transition pairs 
    def test_time_combinations_exist(self):
        set1 = set()
        set2 = set()
        for line in self.linedict:
            for stop in self.linedict[line]:
                if self.linedict[line].index(stop) != len(self.linedict[line]) - 1:
                    set1.add(
                        (stop, self.linedict[line][self.linedict[line].index(stop) + 1])
                    )
                    set1.add(
                        (self.linedict[line][self.linedict[line].index(stop) + 1], stop)
                    )

        for time in self.timedict:
            for key in list(self.timedict[time].keys()):
                set2.add((time, key))
                set2.add((key, time))

        self.assertEqual(set1, set2)
    
    #Test the dialogue (answer_query) function 
    def test_dialogue(self):
        for query, answer in self.answers.items():
            self.assertEqual(tramdata.answer_query(self.tramdict, query), answer, msg=query)


if __name__ == "__main__":
    unittest.main()
