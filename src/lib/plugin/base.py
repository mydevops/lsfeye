import json
from typing import Any
from typing import Dict

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from src.db.base import sessionmanager
from src.lib import extension
from src.lib import util


class PluginBase(object):
    def __init__(self, cmd: str, model: Any, unique_key: str):
        self.cmd = cmd
        self.model = model
        self.unique_key = unique_key

    @extension.handle_exceptions
    async def do(self) -> None:
        async with sessionmanager.session() as session:
            data = json.loads(util.execute_shell_command(self.cmd))
            records = {
                record.get(self.unique_key.upper(), ""): record
                for record in data.get("RECORDS", [])
            }

            update_keys = [
                getattr(i, self.unique_key)
                for i in (
                    await session.execute(
                        select(self.model).filter(
                            getattr(self.model, self.unique_key).in_(
                                records.keys()
                            )
                        )
                    )
                ).scalars()
            ]
            create_keys = set(records) - set(update_keys)
            print("ALL", records)
            print("UPDATE", update_keys)
            print("CREATE", create_keys)

            # update
            for key in update_keys:
                await session.execute(
                    update(self.model)
                    .where(getattr(self.model, self.unique_key) == key)
                    .values(self.prepare_values(records[key]))
                )

            # create
            if create_keys:
                await session.execute(
                    insert(self.model),
                    [self.prepare_values(records[key]) for key in create_keys],
                )

            await session.commit()

    def prepare_values(self, record: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError(
            "This method should be overridden in subclasses!"
        )
