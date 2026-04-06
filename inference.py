import logging

def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

from openai import OpenAI
import time
import random
from config import *
from .prompt import build_prompt
from .parser import parse_output
from utils.logger import get_logger

logger = get_logger()


def single_inference(client, text):
    system, user = build_prompt(text)

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"LLM call attempt {attempt+1}")

            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=TEMPERATURE + random.uniform(-0.1, 0.1)
            )

            content = resp.choices[0].message.content
            data = parse_output(content)

            if "sentiment" in data:
                return data

        except Exception as e:
            logger.warning(f"Error: {e}")
            time.sleep(0.5)

    return None


def multi_sample(client, text):
    results = []
    for i in range(N_SAMPLES):
        logger.info(f"Sampling round {i+1}")
        res = single_inference(client, text)
        if res:
            results.append(res)

    return results

