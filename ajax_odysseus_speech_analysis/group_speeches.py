import csv
import xml.etree.ElementTree as ET
from cltk import NLP


class SophocleanDocument:
    NS = {"tei": "http://www.tei-c.org/ns/1.0"}

    def __init__(self, urn) -> None:
        self.tree = ET.parse(f"texts/{urn}.xml")
        self.root = self.tree.getroot()
        self.nlp = NLP(language="grc")

    def findall(self, xpath):
        return self.root.findall(xpath, self.NS)

    def get_speakers(self):
        speakers = [s.text for s in self.findall(".//tei:speaker")]

        return set(speakers)

    def get_lines_by_speaker(self, speaker):
        return self.findall(".//tei:speaker[.='{}']/../tei:l".format(speaker))

    def group_lines(self):
        speakers = self.get_speakers()
        speeches = {}

        for s in speakers:
            lines = [
                (l.attrib["n"], l.text.strip())
                for l in self.get_lines_by_speaker(s)
                if l.text and l.text.strip()
            ]
            speeches[s] = lines

        return speeches

    def write_lines_to_csv(self):
        fieldnames = ["text", "line_number"]
        grouped_lines = self.group_lines()

        for speaker, lines in grouped_lines.items():
            with open(
                "data/{}.csv".format(speaker), "w", newline="", encoding="utf-8"
            ) as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    delimiter=" ",
                    quotechar="|",
                    quoting=csv.QUOTE_MINIMAL,
                )
                for l in lines:
                    text = l[0]

                    if text is not None and text.strip():
                        writer.writerow({"text": text.strip(), "line_number": l[1]})

        return True


class TrachiniaeDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg001.perseus-grc2")


class AntigoneDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg002.perseus-grc2")


class AjaxDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg003.perseus-grc2")


class OTDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg004.perseus-grc2")


class ElectraDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg005.perseus-grc2")


class PhiloctetesDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg006.perseus-grc2")


class OCDocument(SophocleanDocument):
    def __init__(self):
        super().__init__("tlg0011.tlg007.perseus-grc2")


if __name__ == "__main__":
    # get lines by each speaker
    # analyze lines metrically
    # analyze lines semantically
    # analyze lines by TF-IDF
    # textrank comparison of Ajax's and Odysseus's lines in the _Iliad_?
    doc = AjaxDocument()
    doc.write_lines_to_csv()
