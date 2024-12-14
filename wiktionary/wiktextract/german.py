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

from wiktionary.wiktextract.parse import get_part_of_speech

GERMAN_CASES = ["nominative", "genitive", "dative", "accusative"]


def get_gender_modifier(vocabulary) -> str:
    if get_part_of_speech(vocabulary) == "noun" and "categories" in vocabulary:
        if "German masculine nouns" in vocabulary["categories"]:
            return "der "
        if "German feminine nouns" in vocabulary["categories"]:
            return "die "
        if "German neuter nouns" in vocabulary["categories"]:
            return "das "
    return ""


def get_german_inflection(vocabulary) -> dict:
    inflections = {"declension": None, "conjugation": None}
    if get_part_of_speech(vocabulary) == "noun":
        inflections["declension"] = get_german_noun_declensions(vocabulary)
    if get_part_of_speech(vocabulary) == "adj":
        inflections["declension"] = get_german_adj_declensions(vocabulary)
    return inflections


def get_german_adj_declensions(vocabulary) -> dict:
    """
    There will be 3 x 3 list of maps for an adj. declensions with the first 3 corresponding to
    `adj. degree <https://en.wikipedia.org/wiki/Adjective#Comparison_(degrees)>`_:

    1. 3 for regular (positive) form
    2. 3 for comparative form
    3. 3 for mixed form

    and the second 3 corresponding to the declension type of

    1. strong declension
    2. weak declension
    3. mixed declension

    Each list contains 4 maps. Each of the 4 maps is two-key indexed with the 1st index being the number & gender:

    - "masculine"
    - "feminine"
    - "neuter"
    - "plural

    and the 2nd index being the case:

    - "nominative"
    - "genitive"
    - "dative"
    - "accusative"

    An example data source can be found at https://en.wiktionary.org/wiki/mobil#Declension_2

    :param vocabulary: a wiktextract JSONL line corresponding to an adjective (pos = "adj")

    :return: a map with 3 entries, each for corresponds to a adj. degree with 3 corresponding sub-maps, totaling the 9
    maps mentioned above. If the `vocabulary` does not have a `forms` field, where all declension info reside, this
    function returns an empty map
    """
    if "forms" not in vocabulary:
        return {}

    forms = [form for form in vocabulary["forms"] if "source" in form and form["source"] == "declension"]

    numbergenders = ["masculine", "feminine", "neuter", "plural"]

    conjugations = {
        "positive": {"strong": [], "weak": [], "mixed": []},
        "comparative": {"strong": [], "weak": [], "mixed": []},
        "superlative": {"strong": [], "weak": [], "mixed": []},
    }

    for degree in conjugations.keys():
        for declension_type in ["strong", "weak", "mixed"]:
            for numbergender in numbergenders:
                dec_by_case = {}
                for case in GERMAN_CASES:
                    for declension in forms:
                        tags = declension["tags"]
                        if (degree in tags or degree == "positive") and declension_type in tags:
                            if numbergender in tags and case in tags:
                                if declension["form"]:
                                    dec_by_case[case] = declension["form"]
                if len(dec_by_case) > 0:
                    conjugations[degree][declension_type].append(dec_by_case)

    return conjugations


def get_german_noun_declensions(vocabulary):
    if "forms" not in vocabulary:
        return {}

    forms = [form for form in vocabulary["forms"] if "source" in form and form["source"] == "declension"]

    numbers = ["singular", "plural"]

    declensions = {}
    for number in numbers:
        dec_by_case = {}
        for case in GERMAN_CASES:
            for declension in forms:
                tags = declension["tags"]
                if number in tags and case in tags:
                    if declension["form"]:
                        dec_by_case[case] = declension["form"]
        if len(dec_by_case) > 0:
            declensions[number] = dec_by_case

    return declensions
