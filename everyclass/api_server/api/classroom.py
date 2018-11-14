from flask_restplus import Namespace, Resource

api = Namespace('classroom', description='教室相关')


@api.route('/<string:classroom_id>/<string:semester>')
@api.doc(params={'classroom_id': '教室 ID',
                 'semester'    : '学期，格式为 2018-2019-1'})
class Classroom(Resource):
    def get(self, classroom_id, semester):
        """
        获取教室活动
        """
        return {'res': classroom_id,
                'sem': semester}