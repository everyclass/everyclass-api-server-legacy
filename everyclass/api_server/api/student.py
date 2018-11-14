from flask_restplus import Namespace, Resource, fields

api = Namespace('student', description='学生相关')

student_fields = api.model('Student', {
    'id'       : fields.String(description='学生 ID', example='============'),
    'student_no': fields.String(description='学号', example='3901160407'),
    'name'      : fields.String(description='姓名'),
    'class'     : fields.String(description='班级', example='软件1604'),
    'deputy'    : fields.String(description='学院', example='软件学院'),
    'campus'    : fields.String(description='所在校区', example='铁道')
})


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
    @api.marshal_with(student_fields)
    @api.doc(responses={403: 'Not Authorized'})
    def get(self, student_id, semester):
        """
        获取学生基本信息
        """
        return {'hello': id}, 200
