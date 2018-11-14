from flask_restplus import Namespace, Resource

api = Namespace('teacher', description='老师相关')


@api.route('/<string:teacher_id>/schedule/<string:semester>')
@api.doc(params={'teacher_id': '教师 ID',
                 'semester'  : '学期，格式为 2018-2019-1'})
class TeacherSchedule(Resource):
    def get(self, teacher_id, semester):
        """
        获取老师在指定学期的课表
        """
        return {'res': teacher_id,
                'sem': semester}
