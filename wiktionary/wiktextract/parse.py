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

def get_part_of_speech(vocabulary) -> str:
    return vocabulary["pos"] if "pos" in vocabulary else "Unknown"


def get_definitions(vocabulary) -> list:
    return [sense["glosses"][0] if "glosses" in sense else sense["raw_glosses"][0] for sense in vocabulary["senses"] if
            "glosses" in sense or "raw_glosses" in sense]


def get_audios(vocabulary) -> list:
    audios = []
    if "sounds" in vocabulary:
        for sound in vocabulary["sounds"]:
            audio = {}
            if "ogg_url" in sound and sound["ogg_url"] is not None:
                audio["ogg_url"] = sound["ogg_url"]
            if "mp3_url" in sound and sound["mp3_url"] is not None:
                audio["mp3_url"] = sound["mp3_url"]
            if len(audio) > 0:
                audios.append(audio)
    return audios
