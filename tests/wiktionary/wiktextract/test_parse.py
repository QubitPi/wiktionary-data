# Copyright Jiaqi Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from wiktionary.wiktextract.parse import get_audios
from wiktionary.wiktextract.parse import get_definitions


class TestParse(unittest.TestCase):

    def test_get_definitions(self):
        self.assertEqual(
            [],
            get_definitions({"senses": []}),
        )

    def test_get_definitions_empty(self):
        self.assertEqual(
            ["Volapük"],
            get_definitions({
                "senses": [
                    {
                        "glosses": [
                            "Volapük"
                        ]
                    }
                ]
            }),
        )

        self.assertEqual(
            ["Volapük"],
            get_definitions({
                "senses": [
                    {
                        "raw_glosses": [
                            "Volapük"
                        ]
                    }
                ]
            }),
        )

    def test_get_audios(self):
        self.assertEqual(
            [{
                "ogg_url": "https://upload.wikimedia.org/wikipedia/commons/a/a8/De-Volap%C3%BCk.ogg",
                "mp3_url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a8/De-Volap%C3%BCk.ogg/" +
                           "De-Volap%C3%BCk.ogg.mp3"
            }],
            get_audios({
                "sounds": [
                    {
                        "ipa": "/ˌvoːlaˈpyːk/"
                    },
                    {
                        "ipa": "/ˌvɔla-/"
                    },
                    {
                        "audio": "De-Volapük.ogg",
                        "ogg_url": "https://upload.wikimedia.org/wikipedia/commons/a/a8/De-Volap%C3%BCk.ogg",
                        "mp3_url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a8/" +
                                   "De-Volap%C3%BCk.ogg/De-Volap%C3%BCk.ogg.mp3"
                    }
                ]
            })
        )
