from flask_restplus import Namespace, Resource

api = Namespace('course', description='课程相关')


@api.route('/<string:course_id>/<string:semester>')
@api.doc(params={'course_id': '课程 ID',
                 'semester' : '学期，格式为 2018-2019-1'})
class Course(Resource):
    def get(self, course_id, semester):
        """
        获取一门课程的详情
        """
        return {'res': course_id,
                'sem': semester}
