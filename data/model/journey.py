from dataclasses import dataclass
import uuid
from geojson import Point, LineString


@dataclass
class Journey:
    id: uuid.uuid4
    start_pos: Point
    end_pos: Point
    path: LineString
    duration_seconds: int
