from flask_restful import Resource
from flask import request
from marshmallow import  fields
from sqlalchemy import or_, and_, text



from models.option import OptionModel
from schemas.option import OptionSchema


DATA_NOT_FOUND = 'The data was not found.'
CREATED_SUCCESSFULLY = "A data created successfully."
UPDATED_SUCCESSFULLY = "A data has updated successfully."
DATA_DELETED = "A data has been deleted."

option_schema = OptionSchema()
options_schema = OptionSchema(many=True)


class OptionList(Resource):
    @classmethod
    def get(cls):
        args = request.args
        page = args.get('page',1)
        per_page = args.get('pagesize',10)

        sort = args.get('orderby','id')
        if args.get('desc', 0, int)>0:
            sort = args.get('orderby') + ' desc'
        
    

        result = {
            'pagination':{
                'total':pagination.total,
                'pageSize': pagination.per_page,
                'current': pagination.page
            }
        }

        return result, 200

class Option(Resource):
    @classmethod
    def get(cls, option_id: int):
        option = OptionModel.find_by_id(option_id)
        if not option:
            return {"message": DATA_NOT_FOUND}, 404

        return option_schema.dump(option), 200

    @classmethod
    def post(cls):
        option_json = request.get_json()
        print(option_json)
        option = option_schema.load(option_json)
        option.save_to_db()

        # for item_json in report_items_json:
        #     # 只载入部分数据(Report_id原为必须字段) 参见： https://marshmallow.readthedocs.io/en/stable/quickstart.html#partial-loading
        #     item = report_item_schema.load(item_json, partial=("report_id",))
        #     item.report_id = report.id
        #     item.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

    @classmethod
    def put(cls, option_id: int):
        option_json = request.get_json()
        option = OptionModel.find_by_id(option_id)

        if not option:
            return {"message": DATA_NOT_FOUND}, 404


        # if 'plan' in report_json.keys():
        #     report.plan = report_json['plan']

        option.update()
        return {"message": UPDATED_SUCCESSFULLY}, 201
    
    @classmethod
    def delete(cls, option_id: int):

        option = OptionModel.find_by_id(option_id)
        if not option:
            return {"message": DATA_NOT_FOUND}, 404

        option.delete_from_db()
        return {"message": DATA_DELETED}, 200

# class ReportItem(Resource):
#     @classmethod
#     def get(cls, item_id: int):
#         report_item = ReportItemModel.find_by_id(item_id)
#         if not report_item:
#             return {"message": REPORT_ITEM_NOT_FOUND}, 404

#         return report_item_schema.dump(report_item), 200

#     @classmethod
#     def post(cls):
#         report_item_json = request.get_json()
#         report_item = report_item_schema.load(report_item_json)
#         report_item.save_to_db()

#         return {"message": REPORT_ITEM_CREATED_SUCCESSFULLY}, 201

#     @classmethod
#     def put(cls, item_id: int):
#         report_item_json = request.get_json()
#         report_item = ReportItemModel.find_by_id(item_id)

#         if not report_item:
#             return {"message": REPORT_ITEM_NOT_FOUND}, 404

#         if 'duration' in report_item_json.keys():
#             report_item.duration = report_item_json['duration']

#         if 'content' in report_item_json.keys():
#             report_item.content = report_item_json['content']

#         report_item.update()
#         return {"message": REPORT_ITEM_UPDATED_SUCCESSFULLY}, 201


#     @classmethod
#     def delete(cls, item_id: int):

#         report_item = ReportItemModel.find_by_id(item_id)
#         if not report_item:
#             return {"message": REPORT_ITEM_NOT_FOUND}, 404

#         report_item.delete_from_db()
#         return {"message": REPORT_ITEM_DELETED}, 200