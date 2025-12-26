import yaml
from pathlib import Path
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from config.config import settings as cfg


class Bot:
    def __init__(
            self,
            system_prompt: str,
            examples_path: str = "few-shot-prompts/examples.yaml",
            k: int = 2,
    ):
        self.system_prompt = system_prompt
        self.k = k
        self.chat_model = ChatOpenAI(
            model=cfg.openrouter.OPENROUTER_MODEL,
            api_key=cfg.openrouter.OPENROUTER_API_KEY,
            base_url=cfg.openrouter.OPENROUTER_URL,
            temperature=0,
            request_timeout=20
        )

        self.embeddings = HuggingFaceEmbeddings(model_name=cfg.huggingface.EMBEDDINGS_MODEL)

        self.examples = self._load_examples(examples_path)

        self.example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples=self.examples,
            embeddings=self.embeddings,
            vectorstore_cls=Chroma,
            k=self.k,
        )

        self.prompt = self._build_prompt()

    @staticmethod
    def _load_examples(path: str) -> list[dict[str, str]]:
        """Загрузка примеров из YAML файла"""
        full_path = Path(path).resolve()
        if not full_path.exists():
            raise FileNotFoundError(f"Examples file not found: {full_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["examples"]

    def _build_prompt(self) -> FewShotPromptTemplate:
        """Создание промпта с примерами"""
        example_template = """
                            Вопрос: {question}
                            Ответ: {answer}
                            """.strip()

        example_prompt = PromptTemplate(
            input_variables=["question", "answer"],
            template=example_template
        )

        few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.example_selector,
            example_prompt=example_prompt,
            prefix=self.system_prompt,
            suffix="Вопрос: {input}\nОтвет:",
            input_variables=["input"],
            example_separator="\n\n",
            template_format="jinja2"
        )
        return few_shot_prompt

    def ask(self, question: str) -> str:
        # Формируем полный промпт
        full_prompt = self.prompt.format(input=question)
        # Передаём в модель
        response = self.chat_model.invoke(full_prompt)
        return response.content
