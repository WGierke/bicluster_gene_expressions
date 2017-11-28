import csv
from io import StringIO
from ..config import EXTERNAL_DATA_PATH
import os
import requests
import json

STRING_DB_INTERACTIONS_QUERY = "http://string-db.org/api/psi-mi-tab/interactionsList?identifiers={identifier}&required_score={min_score}"
STRING_DB_IDENTIFIERS_QUERY = "http://string-db.org/api/json/resolveList?identifiers={identifier}"
DEFAULT_IDENTIFIER = 'ENSP00000362116'
DEFAULT_MIN_SCORE = 400


def get_string_db_identifier(identifier='ENSP00000362116'):
    result = requests.get(STRING_DB_IDENTIFIERS_QUERY.format(**locals()))
    identifiers = result.json()
    homo_sapiens_match = None
    for match_identifier in identifiers:
        if 'Homo sapiens' in match_identifier.values():
            if not homo_sapiens_match:
                homo_sapiens_match = match_identifier
            else:
                raise ValueError("Two matching identifiers for {} in a human found: {}".format(identifier, identifiers))
    return homo_sapiens_match['stringId']


def get_string_db_genes(identifier=DEFAULT_IDENTIFIER, min_score=DEFAULT_MIN_SCORE):
    result = requests.get(STRING_DB_INTERACTIONS_QUERY.format(**locals()))
    return result.text


def get_associated_genes(identifier=DEFAULT_IDENTIFIER, min_score=DEFAULT_MIN_SCORE):
    """

    :param identifier: Identifier of the gene e.g. ENSP00000362116 or PGC
    :param min_score: Minimal confidence score of the association
    :return: List of tuples of gene string, gene name and confidence score
    """
    content = get_string_db_genes(**locals())
    f = StringIO(str(content))
    gene_scores = []
    reader = csv.reader(f, delimiter='\t')
    # Check for each row whether the gene string or gene name contains the identifier
    # Add the remaining game to the associated gene list
    for row in reader:
        gene1_string, gene2_string, gene1_name, gene2_name, _, _, _, _, _, _, _, _, _, _, scores = row
        if identifier in gene1_string or identifier in gene1_name:
            gene_scores.append((gene2_string, gene2_name, scores))
            continue
        if identifier in gene2_string or identifier in gene2_name:
            gene_scores.append((gene1_string, gene1_name, scores))
            continue
    return gene_scores

def save_associated_genes(identifiers=[DEFAULT_IDENTIFIER]):
    for identifier in identifiers:
        try:
            string_db_identifier = get_string_db_identifier(identifier)
        except Exception as e:
            print("Exception with {}: {}".format(identifier, e))
            continue

        file_path = os.path.join(EXTERNAL_DATA_PATH, "{}.json".format(identifier))
        if os.path.isfile(file_path):
            continue

        associated_genes = get_associated_genes(string_db_identifier)
        associated_list = []
        for gene in associated_genes:
            associated_list.append({'string': gene[0], 'name': gene[1], 'score': gene[2]})
        with open(file_path, 'w') as f:
            f.write(json.dumps(associated_list))