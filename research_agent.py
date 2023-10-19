# Description: Research assistant class that handles the research process for a given question.

import json
import os

# libraries
import asyncio

from models.gpt.gpt_messages import generate as ge
from models.web import prompts
from models.web.config import Config
from models.web.text import \
    write_to_file, \
    create_message, \
    read_txt_files, \
    write_md_to_pdf
from models.web.web_scrape import async_browse
from models.web.web_search import web_search

CFG = Config()


class ResearchAgent:
    def __init__(self, question, agent, dire, websocket):
        """ Initializes the research assistant with the given question.
        Args: question (str): The question to research
        Returns: None
        """

        self.question = question
        self.agent = agent
        self.agent_role_prompt = agent
        self.visited_urls = set()
        self.research_summary = ""
        self.directory_name = dire
        self.dir_path = os.path.dirname(f"./outputs/{self.directory_name}/")
        self.websocket = websocket

    async def summarize(self, text, topic):
        """ Summarizes the given text for the given topic.
        Args: text (str): The text to summarize
                topic (str): The topic to summarize the text for
        Returns: str: The summarized text
        """

        messages = [create_message(text, topic)]
        await self.websocket.send_json({"type": "logs", "output": f"📝 Summarizing text for query: {text}"})

        return ge(
            messages=messages,
            model=CFG.fast_llm_model
        )

    async def get_new_urls(self, url_set_input):
        """ Gets the new urls from the given url set.
        Args: url_set_input (set[str]): The url set to get the new urls from
        Returns: list[str]: The new urls from the given url set
        """

        new_urls = []
        for url in url_set_input:
            if url not in self.visited_urls:
                await self.websocket.send_json({"type": "logs", "output": f"✅ Adding source url to research: {url}\n"})
                self.visited_urls.add(url)
                new_urls.append(url)

        return new_urls

    async def call_agent(self, action):
        messages = [{
            "role": "system",
            "content": self.agent_role_prompt if self.agent_role_prompt else prompts.generate_agent_role_prompt(
                self.agent)
        }, {
            "role": "user",
            "content": action,
        }]
        answer = ge(
            model=CFG.smart_llm_model,
            messages=messages
        )
        print(answer)
        await self.websocket.send_json({"type": "logs", "output": answer})
        return answer

    async def create_search_queries(self):
        result = await self.call_agent(prompts.generate_search_queries_prompt(self.question))
        print(result)
        return json.loads(result)

    async def async_search(self, query):
        search_results = json.loads(web_search(query))
        new_search_urls = self.get_new_urls([url.get("href") for url in search_results])
        await self.websocket.send_json(
            {"type": "logs",
             "output": f"🌐 Browsing the following sites for relevant information: {new_search_urls}..."})

        # Create a list to hold the coroutine objects
        tasks = [async_browse(url, query) for url in await new_search_urls]

        # Gather the results as they become available
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return responses

    async def run_search_summary(self, query):
        await self.websocket.send_json({"type": "logs", "output": f"🔎 Running research for '{query}'..."})
        responses = await self.async_search(query)

        result = "\n".join(responses)
        os.makedirs(os.path.dirname(f"{self.directory_name}/research-{query}.txt"), exist_ok=True)
        write_to_file(f"{self.directory_name}/research-{query}.txt", result)
        return result

    async def conduct_research(self):
        """ Conducts the research for the given question.
        Args: None
        Returns: str: The research for the given question
        """

        self.research_summary = read_txt_files(self.dir_path) if os.path.isdir(self.dir_path) else ""

        if not self.research_summary:
            search_queries = await self.create_search_queries()
            for query in search_queries:
                research_result = await self.run_search_summary(query)
                self.research_summary += f"{research_result}\n\n"
        await self.websocket.send_json(
            {"type": "logs", "output": f"Total research words: {len(self.research_summary.split(' '))}"})

        return self.research_summary

    async def create_concepts(self):
        """ Creates the concepts for the given question.
        Args: None
        Returns: list[str]: The concepts for the given question
        """
        result = self.call_agent(prompts.generate_concepts_prompt(self.question, self.research_summary))
        await self.websocket.send_json(
            {"type": "logs", "output": f"I will research based on the following concepts: {result}\n"})
        return json.loads(result)

    async def write_report(self, report_type):
        """ Writes the report for the given question.
        Args: None
        Returns: str: The report for the given question
        """
        report_type_func = prompts.get_report_by_type(report_type)
        await self.websocket.send_json(
            {"type": "logs", "output": f"✍️ Writing {report_type} for research task: {self.question}..."})

        answer = await self.call_agent(report_type_func(self.question, self.research_summary))

        path = await write_md_to_pdf(report_type, self.directory_name, answer)

        return answer, path

    async def write_lessons(self):
        """ Writes lessons on essential concepts of the research.
        Args: None
        Returns: None
        """
        concepts = await self.create_concepts()
        for concept in concepts:
            answer = await self.call_agent(prompts.generate_lesson_prompt(concept))
            await write_md_to_pdf("Lesson", self.directory_name, answer)
