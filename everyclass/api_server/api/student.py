from flask_restplus import Namespace, Resource

api = Namespace('student', description='学生相关')


@api.route('/<string:student_id>/schedule/<string:semester>')
@api.doc(params={'student_id': '学生 ID',
                 'semester'  : '学期，格式为 2018-2019-1'})
class StudentSchedule(Resource):
    def get(self, student_id, semester):
        """
        获取学生在指定学期的课表
        """
        return {'hello': id}, 200


@api.route('/<string:student_id>')
@api.doc(params={'student_id': '学生 ID'})
class Student(Resource):
    @api.doc(security=[{'apikey': ['read'], 'oauth2': ['read']}])
    def get(self, student_id, semester):
        """
        获取学生基本信息
        """
        return {'hello': id}, 200
