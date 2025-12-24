import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, ValidationError
from src.config.config import settings as cfg


class WeatherInfo(BaseModel):
    city: str
    temperature: float
    condition: str


def main():
    llm = ChatOpenAI(
        model=cfg.openrouter.OPENROUTER_MODEL,
        api_key=cfg.openrouter.OPENROUTER_API_KEY,
        base_url=cfg.openrouter.OPENROUTER_URL,
        temperature=0,
        request_timeout=20
    )

    output_parser = PydanticOutputParser(pydantic_object=WeatherInfo)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=(
            "Ответь на вопрос в требуемом формате.\n"
            "{format_instructions}\n"
            "Вопрос: {user_question}\nОтвет:"
        ),
        input_variables=["user_question"],
        partial_variables={"format_instructions": format_instructions},
    )

    chain = prompt | llm | output_parser

    try:
        city = input("Введите город: ").strip()
        if not city:
            raise ValueError("Город не может быть пустым.")

        result = chain.invoke({"user_question": f"Текущая погода в городе {city}"})

        print(result.model_dump_json(indent=2, ensure_ascii=False))

    except ValidationError as e:
        print(json.dumps({"error": "Invalid response format", "details": str(e)}, ensure_ascii=False, indent=2))
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": "Failed to get weather info", "details": str(e)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()