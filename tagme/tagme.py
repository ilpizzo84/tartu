import requests
import simplejson


class TagMe:
    """
    A Python wrapper for the TagMe REST API, which provides a text annotation service:
    https://tagme.d4science.org/tagme/
    It is able to identify on-the-fly meaningful short-phrases (called "spots") in an unstructured text and link them
    to a pertinent Wikipedia page in a fast and effective way. English and Italian languages are supported.
    Methods:
        - query_tagme: post the proper query to the REST API service, and return the JSON reply.
        - get_entities: process the JSON reply from the REST API, discarding uncertain annotations according to a
        parametric threshold.
    Input:
        - token (mandatory): a string containing the user token for accessing the REST API service.
    """

    def __init__(self, token):

        self.api = "https://tagme.d4science.org/tagme/tag"
        self.token = token

    def query_tagme(self, text, lang):
        """
        Post the proper query to the REST API service, and return the JSON reply.
        Input:
            - text (mandatory): a string containing an unstructured text to be annotated;
            - lang (mandatory): a string identifier representing the text language. Must be one out of ["en", "it"].
        Output:
            - the JSON reply from the REST API.
        """
        payload = {"text": text, "gcube-token": self.token, "lang": lang}
        if len(text) > 4000:
            payload["long_text"] = 3
        r = requests.post(self.api, payload)
        if r.status_code != 200:
            print(r.content)
            return None
        return simplejson.loads(r.content)

    @staticmethod
    def get_entities(tagme_response, min_rho):
        """
        Process the JSON reply from the REST API, discarding uncertain annotations according to a parametric threshold.
        Input:
        - tagme_response (mandatory): the JSON reply from the REST API.
        - min_rho: a float in [0, 1.0) interval. Annotation with rho <= min_rho are discarded.
        Output:
        - a list, containing the filtered annotations.
        """

        ann = tagme_response["annotations"]
        ann = filter(lambda d: float(d["rho"]) > min_rho, ann)
        return list(map(lambda d: d["title"], ann))
