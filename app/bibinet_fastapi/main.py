import json
import os

import asyncpg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse


env = os.path.join(os.path.dirname(__file__), "../env/.env.dev")
load_dotenv(dotenv_path=env)

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()


async def get_db_pool():
    pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        yield pool
    finally:
        await pool.close()


@app.post("/api/search/part/")
async def search_parts(request: Request, pool=Depends(get_db_pool)):
    data = await request.json()
    mark_name = data.get("mark_name")
    part_name = data.get("part_name")
    params = data.get("params", {})
    color = params.get("color")
    is_new_part = params.get("is_new_part")
    price_gte = data.get("price_gte")
    price_lte = data.get("price_lte")
    page = data.get("page", 1)

    query = """
        SELECT
            p.id,
            p.name,
            p.json_data,
            p.price,
            m.id AS mark_id,
            m.name AS mark_name,
            m.producer_country_name,
            mo.id AS model_id,
            mo.name AS model_name
        FROM
            parts_part p
        JOIN
            parts_mark m ON p.mark_id = m.id
        JOIN
            parts_model mo ON p.model_id = mo.id
        WHERE
            p.is_visible = TRUE
        """
    filters = []
    params_list = []
    param_counter = 1

    if mark_name:
        filters.append(f"m.name ILIKE ${param_counter}")
        params_list.append(f"%{mark_name}%")
        param_counter += 1
    if part_name:
        filters.append(f"p.name ILIKE ${param_counter}")
        params_list.append(f"%{part_name}%")
        param_counter += 1
    if color:
        filters.append(f"p.json_data->>'color' ILIKE ${param_counter}")
        params_list.append(f"%{color}%")
        param_counter += 1
    if is_new_part is not None:
        filters.append(f"p.json_data->>'is_new_part' = ${param_counter}")
        params_list.append(str(is_new_part).lower())
        param_counter += 1
    if price_gte is not None:
        filters.append(f"p.price >= ${param_counter}")
        params_list.append(price_gte)
        param_counter += 1
    if price_lte is not None:
        filters.append(f"p.price <= ${param_counter}")
        params_list.append(price_lte)
        param_counter += 1

    if filters:
        query += " AND " + " AND ".join(filters)

    query += f" OFFSET ${param_counter} LIMIT 10"
    params_list.append((page - 1) * 10)

    async with pool.acquire() as connection:
        results = await connection.fetch(query, *params_list)

        parts = []
        for result in results:
            json_data = result["json_data"]
            if isinstance(json_data, str):
                json_data = json.loads(json_data)

            parts.append(
                {
                    "id": result["id"],
                    "mark": {
                        "id": result["mark_id"],
                        "name": result["mark_name"],
                        "producer_country_name": result[
                            "producer_country_name"
                        ],
                    },
                    "model": {
                        "id": result["model_id"],
                        "name": result["model_name"],
                    },
                    "name": result["name"],
                    "json_data": {
                        "color": json_data.get("color", ""),
                        "count": json_data.get("count", 0),
                        "is_new_part": json_data.get("is_new_part", False),
                    },
                    "price": float(result["price"]),
                }
            )

        count_query = """
            SELECT
                COUNT(*)
            FROM
                parts_part p
            JOIN
                parts_mark m ON p.mark_id = m.id
            JOIN
                parts_model mo ON p.model_id = mo.id
            WHERE
                p.is_visible = TRUE
            """
        if filters:
            count_query += " AND " + " AND ".join(filters)

        total_count = await connection.fetchval(count_query, *params_list[:-1])

    response_data = {
        "response": parts,
        "count": total_count,
        "summ": float(sum(part["price"] for part in parts)),
    }

    return JSONResponse(content=response_data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
