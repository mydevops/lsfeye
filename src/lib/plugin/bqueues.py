import json

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from src.db.base import sessionmanager
from src.db.bqueues import BQueuesModel
from src.lib import extension
from src.lib import util


CMD = (
    "bqueues -o \\'queue_name description priority status max jl_u jl_p jl_h"
    " njobs pend run susp rsv ususp ssusp nice\\' -json"
)


@extension.handle_exceptions
async def do() -> None:
    async with sessionmanager.session() as session:
        data = json.loads(util.execute_shell_command(CMD))
        queues = {
            record.get("QUEUE_NAME", ""): record
            for record in data.get("RECORDS", [])
        }

        update_queues = [
            i.queue_name
            for i in (
                await session.execute(
                    select(BQueuesModel).filter(
                        BQueuesModel.queue_name.in_(queues.keys())
                    )
                )
            ).scalars()
        ]

        create_queues = set(queues) - set(update_queues)

        # update
        for queue_name in update_queues:
            await session.execute(
                update(BQueuesModel)
                .where(BQueuesModel.queue_name == queue_name)
                .values(
                    {
                        "description": queues[queue_name].get("DESCRIPTION"),
                        "priority": queues[queue_name].get("PRIORITY") or None,
                        "status": queues[queue_name].get("STATUS"),
                        "max": queues[queue_name].get("MAX") or None,
                        "jl_u": queues[queue_name].get("JL_U") or None,
                        "jl_p": queues[queue_name].get("JL_P") or None,
                        "jl_h": queues[queue_name].get("JL_H") or None,
                        "njobs": queues[queue_name].get("NJOBS") or None,
                        "pend": queues[queue_name].get("PEND") or None,
                        "run": queues[queue_name].get("RUN") or None,
                        "susp": queues[queue_name].get("SUSP") or None,
                        "rsv": queues[queue_name].get("RSV") or None,
                        "ususp": queues[queue_name].get("USUSP") or None,
                        "ssusp": queues[queue_name].get("SSUSP") or None,
                        "nice": queues[queue_name].get("NICE") or None,
                    }
                )
            )
        # create
        if create_queues:
            await session.execute(
                insert(BQueuesModel),
                [
                    {
                        "queue_name": queue_name,
                        "description": queues[queue_name].get("DESCRIPTION"),
                        "priority": queues[queue_name].get("PRIORITY") or None,
                        "status": queues[queue_name].get("STATUS"),
                        "max": queues[queue_name].get("MAX") or None,
                        "jl_u": queues[queue_name].get("JL_U") or None,
                        "jl_p": queues[queue_name].get("JL_P") or None,
                        "jl_h": queues[queue_name].get("JL_H") or None,
                        "njobs": queues[queue_name].get("NJOBS") or None,
                        "pend": queues[queue_name].get("PEND") or None,
                        "run": queues[queue_name].get("RUN") or None,
                        "susp": queues[queue_name].get("SUSP") or None,
                        "rsv": queues[queue_name].get("RSV") or None,
                        "ususp": queues[queue_name].get("USUSP") or None,
                        "ssusp": queues[queue_name].get("SSUSP") or None,
                        "nice": queues[queue_name].get("NICE") or None,
                    }
                    for queue_name in create_queues
                ],
            )

        await session.commit()
