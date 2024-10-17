from time import time
import asyncio
from multiprocessing import Process

from BMW.utils import console


class BackgroundProcess(Process):
    def __init__(self, connection_manager) -> None:
        super().__init__(target=background_process, args=(connection_manager,))


def background_process(connection_manager):
    import BMW.Manager

    BMW.Manager.connection_manager = connection_manager
    asyncio.run(background_process_loop())


async def background_process_loop():
    with console.status("handleing BackgroundProcessLoop") as status:
        while True:
            try:
                await asyncio.sleep(0.5)
                start_time = time()
                ...
                end_time = time()
                status.update(
                    status=f"background process loop cost {end_time - start_time :.4f} seconds"
                )
            except Exception as e:
                console.print_exception()
