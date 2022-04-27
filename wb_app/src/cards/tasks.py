from main.celery import celery_app


@celery_app.task
def get_and_update_good_info():
    print(f'Retrieving data for ')


# @celery_app.on_after_finalize.connect
# def setup_periodic_tasks(**kwargs):
#     celery_app.add_periodic_task(
#         10.0,
#         get_and_update_good_info.s(),
#         name='update good info',
#     )