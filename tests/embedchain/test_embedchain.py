import os
import unittest
from unittest.mock import patch

from embedchain import App
from embedchain.config import AppConfig


class TestChromaDbHostsLoglevel(unittest.TestCase):
    os.environ["OPENAI_API_KEY"] = "test_key"

    @patch("chromadb.api.models.Collection.Collection.add")
    @patch("chromadb.api.models.Collection.Collection.get")
    @patch("embedchain.embedchain.EmbedChain.retrieve_from_database")
    @patch("embedchain.embedchain.EmbedChain.get_answer_from_llm")
    @patch("embedchain.embedchain.EmbedChain.get_llm_model_answer")
    def test_whole_app(
        self,
        _mock_get,
        _mock_add,
        _mock_ec_retrieve_from_database,
        _mock_get_answer_from_llm,
        mock_ec_get_llm_model_answer,
    ):
        """
        Test if the `App` instance is initialized without a config that does not contain default hosts and ports.
        """
        config = AppConfig(log_level="DEBUG", collect_metrics=False)

        app = App(config)

        knowledge = "lorem ipsum dolor sit amet, consectetur adipiscing"

        app.add_local("text", knowledge)

        app.query("What text did I give you?")
        app.chat("What text did I give you?")

        self.assertEqual(mock_ec_get_llm_model_answer.call_args[1]["documents"], [knowledge])

    def test_add_after_reset(self):
        """
        Test if the `App` instance is correctly reconstructed after a reset.
        """
        app = App()
        app.reset()

        # Make sure the client is still healthy
        app.db.client.heartbeat()
        # Make sure the collection exists, and can be added to
        app.collection.add(
            embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2]],
            metadatas=[
                {"chapter": "3", "verse": "16"},
                {"chapter": "3", "verse": "5"},
                {"chapter": "29", "verse": "11"},
            ],
            ids=["id1", "id2", "id3"],
        )

        app.reset()
