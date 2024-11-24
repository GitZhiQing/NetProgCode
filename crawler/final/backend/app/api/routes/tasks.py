from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


@router.post("/crawl_latest")
async def crawl_latest(target_id: int, count: int, background_tasks: BackgroundTasks):
    """
    爬取最新文章
    """
    from app.crawler.main import crawl_range_count

    background_tasks.add_task(crawl_range_count, count=count, target_id=target_id)
    return {"message": "已加入爬取队列"}


@router.post("/crawl_one_id")
async def crawl_one_id_api(
    article_id: int, target_id: int, background_tasks: BackgroundTasks
):
    """
    爬取指定 id 的文章
    """
    from app.crawler.main import crawl_one_id

    background_tasks.add_task(crawl_one_id, article_id, target_id)
    return {"message": "已加入爬取队列"}


@router.post("/crawl_range_id")
async def crawl_range_id_api(
    start_id: int, end_id: int, target_id: int, background_tasks: BackgroundTasks
):
    """
    爬取指定范围 id 的文章
    """
    from app.crawler.main import crawl_range_id

    background_tasks.add_task(
        crawl_range_id, start_id=start_id, end_id=end_id, target_id=target_id
    )
    return {"message": "已加入爬取队列"}


@router.post("/crawl_latest_100")
async def crawl_latest_100(target_id: int, background_tasks: BackgroundTasks):
    """
    爬取最新 100 篇文章
    """
    from app.crawler.main import crawl_range_id

    background_tasks.add_task(
        crawl_range_id, start_id=None, end_id=None, target_id=target_id
    )
    return {"message": "已加入爬取队列"}


@router.post("/preprocess_all")
async def preprocess_all(background_tasks: BackgroundTasks):
    """
    预处理所有文档
    """
    from app.search.preprocess import preprocess_all_odocs

    background_tasks.add_task(preprocess_all_odocs)
    return {"message": "已加入预处理队列"}
