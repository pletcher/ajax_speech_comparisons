from dataclasses import dataclass

import csv
import logging
import sys

from ajax_odysseus_speech_analysis.group_speeches import SophocleanDocument

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@dataclass
class Line:
    n: str
    speaker: str
    raw_text: str
    words: list[any]


class LemmatizedText:
    def __init__(self, urn):
        self.urn = urn
        self.document = SophocleanDocument(self.urn)
        self.speeches = self.document.group_lines()

    def analyze_lines(self, speaker):
        lines = self.speeches[speaker]
        analyzed_lines = []

        for line in lines:
            analyzed = self.document.nlp.analyze(line[1])
            analyzed_lines.append(
                Line(n=line[0], speaker=speaker, raw_text=line[1], words=analyzed.words)
            )

        return analyzed_lines

    def analyze_all_lines_by_speaker(self):
        return dict(
            [
                (speaker, self.analyze_lines(speaker))
                for speaker, _lines in self.speeches.items()
            ]
        )

    def export_to_csv(self):
        fieldnames = [
            "urn",
            "n",
            "speaker",
            "raw_word",
            "pos",
            "lemma",
        ]

        with open(
            f"data/urn:cts:greekLit:{self.urn}.cp-words.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                delimiter="\t",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )

            writer.writeheader()

            for speaker, lines in self.analyze_all_lines_by_speaker().items():
                logging.info(f"Writing lines for {speaker}...\n")
                for line in lines:
                    for word in line.words:
                        raw_word = word.string
                        n = line.n
                        urn = f"urn:cts:greekLit:{self.urn}:{n}@{raw_word}"
                        speaker = line.speaker
                        pos = word.pos
                        lemma = word.lemma

                        writer.writerow(
                            dict(
                                urn=urn,
                                n=n,
                                speaker=speaker,
                                raw_word=raw_word,
                                pos=pos,
                                lemma=lemma,
                            )
                        )


URNS = [
    "tlg0011.tlg001.perseus-grc2",
    "tlg0011.tlg002.perseus-grc2",
    "tlg0011.tlg003.perseus-grc2",
    "tlg0011.tlg004.perseus-grc2",
    "tlg0011.tlg005.perseus-grc2",
    "tlg0011.tlg006.perseus-grc2",
    "tlg0011.tlg007.perseus-grc2",
]


if __name__ == "__main__":
    for urn in URNS:
        lemmatized = LemmatizedText(urn)
        lemmatized.export_to_csv()
