from flask_restplus import Namespace, Resource, fields

api = Namespace('teacher', description='老师相关')

teacher_fields = api.model('Teacher', {
    'id'        : fields.String(description='教师 ID', example='============'),
    'teacher_no': fields.String(description='工号', example='3901160407'),
    'name'      : fields.String(description='姓名'),
    'title'     : fields.String(description='职称', example='教授'),
    'degree'    : fields.String(description='学历', example='博士'),
    'unit'      : fields.String(description='所属单位', example='软件学院')
})


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


@api.route('/<string:teacher_id>')
@api.doc(params={'teacher_id': '教师 ID'})
class Teacher(Resource):
    @api.marshal_with(teacher_fields)
    @api.doc(responses={403: 'Not Authorized'})
    def get(self, teacher_id):
        """
        获取老师基本信息
        """
        return {'hello': id}, 200
