import datetime
from typing import List, Dict

import asyncio
from fastapi import WebSocket

from research_agent import ResearchAgent


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.sender_tasks: Dict[WebSocket, asyncio.Task] = {}
        self.message_queues: Dict[WebSocket, asyncio.Queue] = {}

    async def start_sender(self, websocket: WebSocket):
        queue = self.message_queues[websocket]
        while True:
            message = await queue.get()
            if websocket in self.active_connections:
                await websocket.send_text(message)
            else:
                break

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.message_queues[websocket] = asyncio.Queue()
        self.sender_tasks[websocket] = asyncio.create_task(self.start_sender(websocket))

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.sender_tasks[websocket].cancel()
        del self.sender_tasks[websocket]
        del self.message_queues[websocket]

    async def start_streaming(self, task, report_type, agent, agent_role_prompt, websocket):
        report, path = await run_agent(task, report_type, agent, agent_role_prompt, websocket)
        return report, path


async def run_agent(task, report_type, agent, agent_role_prompt, websocket):
    start_time = datetime.datetime.now()

    # await websocket.send_json({"type": "logs", "output": f"Start time: {str(start_time)}\n\n"})

    assistant = ResearchAgent(task, agent, agent_role_prompt, websocket)
    await assistant.conduct_research()

    report, path = await assistant.write_report(report_type)

    await websocket.send_json({"type": "path", "output": path})

    end_time = datetime.datetime.now()
    await websocket.send_json({"type": "logs", "output": f"\nEnd time: {end_time}\n"})
    await websocket.send_json({"type": "logs", "output": f"\nTotal run time: {end_time - start_time}\n"})

    return report, path
