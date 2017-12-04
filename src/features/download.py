import json
import os

import requests

from ..config import EXTERNAL_DATA_PATH

STRING_DB_INTERACTIONS_QUERY = "http://string-db.org/api/json/interactionsList?identifiers={identifier}&required_score={min_score}"
STRING_DB_IDENTIFIERS_QUERY = "http://string-db.org/api/json/resolveList?identifiers={identifier}&species=9606"
DEFAULT_IDENTIFIER = 'ENSP00000362116'
DEFAULT_MIN_SCORE = 400


def get_string_db_identifier(identifier=DEFAULT_IDENTIFIER):
    result = requests.get(STRING_DB_IDENTIFIERS_QUERY.format(**locals()))
    identifiers = result.json()
    if not identifiers:
        raise ValueError("Identifier is unknown to StringDB: {}".format(identifier))
    homo_sapiens_match = None
    for match_identifier in identifiers:
        if 'Homo sapiens' in match_identifier.values():
            if not homo_sapiens_match:
                homo_sapiens_match = match_identifier
            else:
                raise ValueError("Two matching identifiers for {} in a human found: {}".format(identifier, identifiers))
    return homo_sapiens_match['stringId'].split('9606.')[1]  # Only return the ensemble identifier without the species


def get_string_db_genes(identifier=DEFAULT_IDENTIFIER, min_score=DEFAULT_MIN_SCORE):
    """
    Get the associated genes of an unsafe gene identifier
    :param identifier: unsafe identifier e.g. PGC
    :param min_score: minimal score of the associations
    :return: used StringDB identifier, resulting interactions
    """
    identifier = get_string_db_identifier(identifier)
    result = requests.get(STRING_DB_INTERACTIONS_QUERY.format(**locals()))
    return identifier, result.json()


def get_associated_genes(identifier=DEFAULT_IDENTIFIER, min_score=DEFAULT_MIN_SCORE):
    """

    :param identifier: Identifier of the gene e.g. ENSP00000362116 or PGC
    :param min_score: Minimal confidence score of the association
    :return: List of dict of gene string, gene name and scores with keys 'pscore', 'ascore', 'tscore', 'fscore',
    'escore', 'preferredName', 'stringId', 'nscore', 'ncbiTaxonId', 'score', 'dscore'
    """
    string_db_identifier, association_list = get_string_db_genes(**locals())
    gene_scores = []
    for association in association_list:
        gene1_string, gene2_string = association["stringId_A"], association["stringId_B"]
        if gene1_string in [identifier, string_db_identifier]:
            association["stringId"] = association["stringId_B"]
            association["preferredName"] = association["preferredName_B"]
        elif gene2_string in [identifier, string_db_identifier]:
            association["stringId"] = association["stringId_A"]
            association["preferredName"] = association["preferredName_A"]
        else:
            continue
        del association["stringId_A"]
        del association["stringId_B"]
        del association["preferredName_A"]
        del association["preferredName_B"]
        gene_scores.append(association)
    return gene_scores


def save_associated_genes(identifiers=[DEFAULT_IDENTIFIER]):
    """
    Save the associated genes of the given identifiers to files.
    :param identifiers: gene identifiers, not necessarily validated
    """
    for identifier in identifiers:
        file_path = os.path.join(EXTERNAL_DATA_PATH, "{}.json".format(identifier))
        if os.path.isfile(file_path):
            continue
        associated_genes = get_associated_genes(identifier)
        content = {"identifier": get_string_db_identifier(identifier), "data": associated_genes}
        with open(file_path, 'w') as f:
            f.write(json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')))
        print("Saved associated genes for {}".format(identifier))


def load_associated_genes(identifier=DEFAULT_IDENTIFIER):
    file_path = os.path.join(EXTERNAL_DATA_PATH, "{}.json".format(identifier))
    if not os.path.isfile(file_path):
        save_associated_genes([identifier])

    with open(file_path, 'r') as f:
        content = f.read()
    return json.loads(content)["data"]
