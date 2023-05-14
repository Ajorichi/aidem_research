from criss.cat import aggr as cluster
from database.post import post_pipe as post

def upload(results= dict, srv = dict, database= str):
    pred = []
    cls = list((results[0].names).values())
    for box in results[0].boxes:
        res = results[0].names[box.cls[0].item()]
        pred.append(res)
    res = cluster(fluid = pred, cat = cls, no_cls_agr = True, len_cat = False, set_datetime = True)
    post(data = res, srv=srv, database= database)