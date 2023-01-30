from pathlib import Path, PurePosixPath
from typing import IO, Generator
from django.shortcuts import get_object_or_404

from PNPM import settings
from .models import Video


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        if end:
            data_length = min(block_size, end - start - consumed)
        else:
            data_length = block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, video_id):
    video = get_object_or_404(Video, pk=video_id)

    path = Path(video.file.path)

    file = path.open('rb')

    file_size = path.stat().st_size      # Полный размер файла

    content_size = file_size     # Размер контента
    full_range = request.headers.get('range')   # Запрос байтов  "bytes = 12 - 145"

    status_code = 200

    if full_range is not None:
        content_ranges = full_range.strip().split('=')[-1]     # Диапазон чтения (12 - 145)
        range_start = content_ranges.split('-')[0].strip()     # начало (12)
        range_end = content_ranges.split('-')[-1].strip()      # конец (145)
        if range_start:
            range_start = max(0, int(range_start))
        else:
            range_start = 0
        if range_end:
            range_end = min(file_size - 1, int(range_end))
        else:
            range_end = file_size - 1

        content_size = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        full_range = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_size, full_range
